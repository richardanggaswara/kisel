# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class ProductRequestInherit(models.Model):
    _name = "vit.product.request"
    _inherit = "vit.product.request"
    
    def action_create_pr_baru(self):
        cr = self.env.cr
        purchase_requisition          = self.env['purchase.requisition']
        purchase_requisition_line      = self.env['purchase.requisition.line']   
 
        for prd_req in self:
            pr_line_ids = []
            for lines in prd_req.product_request_line_ids:
                pr_line_ids.append( (0,0,{
                    'analytic_account_id':lines.analytic_account_id.id,
                    'unit_id'       : lines.unit_id.id,
                    'analytic_tag_ids_l'    : lines.analytic_tag_ids.id,
                    'analytic_tag_ids_b': lines.analytic_tag_ids_b.id,
                    'product_id'    : lines.product_id.id,
                    'description'    : lines.name,
                    'product_qty'    : lines.product_qty,
                    'product_uom_id': lines.product_uom_id.id,
                    'schedule_date'    : lines.date_required,
                    'price_unit'    : lines.unit_price,
                }) )
            partner = False
            if prd_req.partner_id:
                partner=self.partner_id.id
            pr_id = purchase_requisition.create({
                'name'            : self.env['ir.sequence'].get('purchase.requisition.purchase.tender'),
                'exclusive'        : 'exclusive',
                'warehouse_id'      : self.warehouse_id.id ,
                'line_ids'         : pr_line_ids,
                'partner_id'        : partner,
                'origin'          : prd_req.name
            })
            #update state dan pr_id di line product request asli
            cr.execute("update vit_product_request_line set state=%s, purchase_requisition_id=%s where product_request_id = %s",
             ( 'onprogress', pr_id.id,  prd_req.id  ))

            self.write({'state':'onprogress'}, )

            body = _("PR bid created")
            self.send_followers()

            return pr_id

class ProductRequestLine(models.Model):
    _name = "vit.product.request.line"
    _inherit = "vit.product.request.line"
    
    def action_create_pr_baru(self, active_ids):
        state_not_open = self.filtered(lambda x: x.state != 'open')
        if state_not_open :
            raise UserError(_('Status product request line harus open (confirmed) !'))
        cr = self.env.cr
        purchase_requisition  = self.env['purchase.requisition']
        product_request       = self.env['vit.product.request']
        prs = {}
        i=0
        sql = "select product_id, product_uom_id, analytic_account_id, unit_id, analytic_tag_ids, analytic_tag_ids_b, name, product_request_id, id, date_required, unit_price, product_qty " \
              "from vit_product_request_line " \
              "where id in %s " \
              "group by product_id, product_uom_id, analytic_account_id, unit_id, analytic_tag_ids, analytic_tag_ids_b, name, product_request_id, id, date_required " \
              "order by product_id, product_uom_id, analytic_account_id, unit_id, analytic_tag_ids, analytic_tag_ids_b, name, product_request_id, id, date_required"
        cr.execute(sql, ( tuple(active_ids),))
        res = cr.dictfetchall()

        pr_line_ids = []
        for r in res:
            analytic_account_id = r['analytic_account_id']
            unit_id = r['unit_id']
            analytic_tag_ids = r['analytic_tag_ids']
            analytic_tag_ids_b = r['analytic_tag_ids_b']
            product_id = r['product_id']
            product_qty = r['product_qty']
            unit_price = r['unit_price']
            pr_line_ids.append( (0,0,{
                    'analytic_account_id': r['analytic_account_id'],
                    'unit_id'       : r['unit_id'],
                    'analytic_tag_ids_l'    : r['analytic_tag_ids'],
                    'analytic_tag_ids_b': r['analytic_tag_ids_b'],
                    'product_id'    : r['product_id'],
                    'description'    : r['name'],
                    'product_qty'    : r['product_qty'],
                    'product_uom_id': r['product_uom_id'],
                    'schedule_date'    : r['date_required'],
                    'price_unit'    : r['unit_price'],
                }) )
        pr_id = purchase_requisition.create({
            'name': self.env['ir.sequence'].get('purchase.requisition.purchase.tender'),
            'exclusive'        : 'exclusive',
            'warehouse_id'      : self.warehouse_id.id ,
            'line_ids'         : pr_line_ids,
        })
        #update state dan pr_id di line product request asli
        cr.execute("update vit_product_request_line set state=%s, purchase_requisition_id=%s where id in %s",
        ( 'onprogress', pr_id.id, tuple(active_ids)))

        self.write({'state':'onprogress'}, )

        return pr_id

class ProductRequestLineWizard(models.TransientModel):

    _name = "vit.product.request.line.wizard"
    _inherit = "vit.product.request.line.wizard"
    _description = "Confirm the selected invoices"

    @api.multi
    def create_agreements(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['vit.product.request.line'].browse(active_ids):
            if record.state != 'open':
                raise UserError(_("Selected PR lines cannot be confirmed as they are not in 'Open' state."))
        record.action_create_pr_baru(active_ids)
        return {'type': 'ir.actions.act_window_close'}

ProductRequestLineWizard()
    
    