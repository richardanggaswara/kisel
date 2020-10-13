from odoo import models, fields, api
from odoo import tools
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class ProductRequestInherit(models.Model):
    _name = "vit.product.request"
    _inherit = "vit.product.request"

    def action_create_po_baru(self):
        _logger.info("################################################")
        cr = self.env.cr
        purchase_order          = self.env['purchase.order']
        purchase_order_line      = self.env['purchase.order.line']

        for prd_req in self:
            if not prd_req.partner_id :
                raise UserError(_('Supplier harus diisi !'))
            po_line_ids = []
            for lines in prd_req.product_request_line_ids:
                po_line_ids.append( (0,0,{
                    'analytic_account_id'   : lines.analytic_account_id.id,
                    'unit_id'               : lines.unit_id.id,
                    'analytic_tag_ids_l'    : lines.analytic_tag_ids.id,
                    'analytic_tag_ids_b'    : lines.analytic_tag_ids_b.id,
                    'product_id'     : lines.product_id.id,
                    'name'           : lines.name,
                    'product_qty'    : lines.product_qty,
                    'product_uom'    : lines.product_uom_id.id,
                    'price_unit'     : lines.unit_price,
                    'date_planned'   : lines.date_required,
                }) )
            po_id = purchase_order.create({
                'name'               : 'New',
                'picking_type_id'    : self.warehouse_id.in_type_id.id ,
                'order_line'         : po_line_ids,
                'partner_id'         : prd_req.partner_id.id,
                'origin'             : prd_req.name
            })
            #update state dan po_id di line product request asli
            cr.execute("update vit_product_request_line set state=%s, purchase_order_id=%s where product_request_id = %s",
             ( 'onprogress', po_id.id,  prd_req.id  ))

            self.write({'state':'onprogress'}, )

            body = _("Purchase Order Created")
            self.send_followers()

            return po_id

class ProductRequestLine(models.Model):
    _name = "vit.product.request.line"
    _inherit = "vit.product.request.line"

    def action_create_po_baru(self, partner_id, warehouse_id, active_ids):
        _logger.info("*****************************************************")
        state_not_open = self.filtered(lambda x: x.state != 'open')
        if state_not_open :
            raise UserError(_('Status product request line harus open (confirmed) !'))
        cr = self.env.cr
        purchase_order  = self.env['purchase.order']
        product_request = self.env['vit.product.request.line']
        origins = product_request.browse(active_ids)
        prs = {}
        i=0
        sql = "select product_id, product_uom_id, warehouse_id, analytic_account_id, unit_id, analytic_tag_ids, analytic_tag_ids_b, name, product_request_id, id, date_required, product_qty, unit_price " \
              "from vit_product_request_line " \
              "where id in %s " \
              "group by product_id, product_uom_id, warehouse_id, analytic_account_id, unit_id, analytic_tag_ids, analytic_tag_ids_b, name, product_request_id, id, date_required " \
              "order by product_id, product_uom_id, warehouse_id, analytic_account_id, unit_id, analytic_tag_ids, analytic_tag_ids_b, name, product_request_id, id, date_required "
        cr.execute(sql, ( tuple(active_ids),))
        res = cr.dictfetchall()

        po_line_ids = []
        for r in res:
            analytic_account_id = r['analytic_account_id']
            unit_id             = r['unit_id']
            analytic_tag_ids    = r['analytic_tag_ids']
            analytic_tag_ids_b  = r['analytic_tag_ids_b']
            product_id          = r['product_id']
            product_qty         = r['product_qty']
            unit_price          = r['unit_price']
            warehouse_id        = r['warehouse_id']
            name                = r['name']
            po_line_ids.append( (0,0,{
                    'analytic_account_id'   : r['analytic_account_id'],
                    'unit_id'               : r['unit_id'],
                    'analytic_tag_ids_l'    : r['analytic_tag_ids'],
                    'analytic_tag_ids_b'    : r['analytic_tag_ids_b'],
                    'product_id'            : r['product_id'],
                    'name'                  : r['name'],
                    'product_qty'           : r['product_qty'],
                    'product_uom'           : r['product_uom_id'],
                    'date_planned'          : r['date_required'],
                    'price_unit'            : r['unit_price'],
                }) )
        po_id = purchase_order.create({
            'name'              : 'New',
            'picking_type_id'   : self.warehouse_id.in_type_id.id ,
            'order_line'        : po_line_ids,
            'partner_id'        : partner_id,
            'origin'            : ",".join( origins.mapped('product_request_id.name') )
        })
        #update state dan po_id di line product request asli
        cr.execute("update vit_product_request_line set state=%s, purchase_order_id=%s where id in %s",
        ( 'onprogress', po_id.id, tuple(active_ids)))

        self.write({'state':'onprogress'}, )

        return po_id

class ProductRequestLineWizardPO(models.TransientModel):

    _name = "vit.product.request.line.wizard.po"
    _inherit = "vit.product.request.line.wizard.po"
    _description = "Confirm the selected invoices"

    partner_id = fields.Many2one("res.partner","Supplier", domain="[('supplier','=',True)]")
    warehouse_id = fields.Many2one("stock.warehouse","Warehouse")

    @api.multi
    def create_po(self):
        _logger.info("=================================================================")
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['vit.product.request.line'].browse(active_ids):
            if record.state != 'open':
                raise UserError(_("Selected PR lines cannot be confirmed as they are not in 'Open' state."))
            record.action_create_po_baru(self.partner_id.id, self.warehouse_id.id, active_ids)
        return {'type': 'ir.actions.act_window_close'}

ProductRequestLineWizardPO()