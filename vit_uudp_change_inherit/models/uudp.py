from odoo import api, fields, models, exceptions, _
import datetime
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.addons.terbilang import terbilang
import logging
_logger = logging.getLogger(__name__)


class uudp(models.Model):
    _name = 'uudp'
    _inherit = 'uudp'
    
    date = fields.Date(string="Project End Date", required=True, default=fields.Date.context_today, track_visibility='onchange',)
    end_date = fields.Date(string="Maximum PJB Date",  track_visibility='onchange',)
    reviewed_by = fields.Many2one(comodel_name='hr.employee',string='Reviewed by')
    budgeted_by = fields.Many2one(comodel_name='hr.employee',string='Budget Confirmed')
    approved_by = fields.Many2one(comodel_name='hr.employee',string='Approved by')
    
    justifikasi = fields.Boolean(string="Justifikasi", track_visibility="onchange")
    pr = fields.Boolean(string="PR", track_visibility="onchange")
    ssph = fields.Boolean(string="SSPH", track_visibility="onchange")
    sph = fields.Boolean(string="SPH", track_visibility="onchange")
    ba_negosiasi = fields.Boolean(string="BA Negosiasi", track_visibility="onchange")
    disposisi = fields.Boolean(string="Disposisi Direksi/GM", track_visibility="onchange")
    surat_penunjukan = fields.Boolean(string="Surat Penunjukan", track_visibility="onchange")
    po_spk = fields.Boolean(string="PO/SPK/Kontrak", track_visibility="onchange")
    baut_bast = fields.Boolean(string="BAUT & BAST", track_visibility="onchange")
    analisa_bisnis = fields.Boolean(string="Analisa Bisnis & Project Report", track_visibility="onchange")
    tanda_terima = fields.Boolean(string="Tanda Terima", track_visibility="onchange")
    invoice_tagihan = fields.Boolean(string="Invoice(Surat Tagihan)", track_visibility="onchange")
    kwitansi = fields.Boolean(string="Kwitansi", track_visibility="onchange")
    faktur_pajak = fields.Boolean(string="Faktur Pajak", track_visibility="onchange")
    bukti_transaksi = fields.Boolean(string="Bukti Transaksi", track_visibility="onchange")
    lpjk            = fields.Boolean(string="LPJK & Enova", track_visibility="onchange")
    ktp             = fields.Boolean(string="KTP", track_visibility="onchange")
    npwp            = fields.Boolean(string="NPWP", track_visibility="onchange")
    lainnya         = fields.Boolean(string="Dokumentasi Lainnya", track_visibility="onchange")

    metode_pengadaan = fields.Selection([('penunjukan_langsung','Penunjukan Langsung'),('pembelian_langsung','Pembelian Langsung'),('dll_npwp','Dan lain-lain(Copy NPWP)')], string="Metode Pengadaan", required=False)
    metode_pembayaran = fields.Selection([('transfer','Transfer')], string="Metode Pembayaran", required=False)
    tahapan_pembayaran = fields.Selection([('dp','DP'),('termin','Termin'),('pelunasan','Pelunasan'),('retensi','Retensi')], string="Tahapan Pembayaran", required=False)
    cara_perolehan = fields.Selection([('pembelian','Pembelian'),('sewa','Sewa'),('sewa_beli','Sewa Beli'),('sewa_guna','Sewa Guna Usaha(Leasing)')], string="Cara Perolehan", required=False)

    vendor = fields.Many2one(comodel_name='res.partner', string="Vendors")
    description_reimberse = fields.Text(string="Description")
    
    prefix_nsfp = fields.Many2one(comodel_name="prefix.nsfp",string="Prefix NSFP")
    efaktur_pajak  = fields.Many2one(comodel_name="vit.efaktur", string="Nomor Seri Faktur Pajak", required=False, )
    journal_payment = fields.Many2one('account.journal', string='Payment Journal', domain=[('type', 'in', ('bank', 'cash'))])

    @api.multi
    def button_done_finance(self):
        if self.type == 'penyelesaian':
            partner = self.ajuan_id.responsible_id.partner_id.id
            total_ajuan = 0
            now = datetime.datetime.now()
            total_ajuan = self.total_ajuan
            if self.uudp_ids:
                account_move_line = []

                total_debit = 0.0
                for ajuan in self.uudp_ids:
                    if not ajuan.coa_debit:
                        raise UserError(_('Account atas %s belum di set!')%(ajuan.description))
                    if ajuan.partner_id :
                        partner = ajuan.partner_id.id
                    tag_id = False
                    if ajuan.store_id :
                        tag_id = [(6, 0, [ajuan.store_id.account_analytic_tag_id.id])]
                    ajuan_total = ajuan.sub_total
                    #account debit
                    if ajuan.sub_total > 0.0 :
                        account_move_line.append((0, 0 ,{'account_id'       : ajuan.coa_debit.id,
                                                         'partner_id'       : partner, 
                                                         'analytic_tag_ids' : tag_id,
                                                         'name'             : ajuan.description, 
                                                         'analytic_account_id': self.department_id.analytic_account_id.id,
                                                         'debit'            : ajuan_total, 
                                                         'date_maturity'    : self.date})) #,
                    elif ajuan.sub_total < 0.0 :
                        account_move_line.append((0, 0 ,{'account_id'       : ajuan.coa_debit.id,
                                                         'partner_id'       : partner, 
                                                         'analytic_tag_ids' : tag_id,
                                                         'name'             : ajuan.description, 
                                                         'analytic_account_id': self.department_id.analytic_account_id.id,
                                                         'credit'            : -ajuan_total, 
                                                         'date_maturity'    : self.date})) #,
                    total_debit += ajuan_total    

                if round(self.sisa_penyelesaian,2) > 0.0:
                    raise AccessError(_('Sisa penyelesaian harus tetap dimasukan ke detail penyelesaian !'))


                account_move_line.append((0, 0 ,{'account_id' : self.ajuan_id.coa_debit.id, 
                                                'partner_id': partner, 
                                                'analytic_account_id':self.department_id.analytic_account_id.id,
                                                'name' : self.notes, 
                                                # 'credit' : total_ajuan, 
                                                'credit' : total_debit, 
                                                'date_maturity':self.date})) #, 

                journal_id = self.ajuan_id.pencairan_id.journal_id
                if not journal_id :
                    journal_id = self.env['account.move'].sudo().search([('ref','ilike','%'+self.ajuan_id.name+'%')],limit=1)
                    if not journal_id :
                        raise AccessError(_('Journal pencairan tidak ditemukan !'))
                    journal_id = journal_id.journal_id
                data={"journal_id":journal_id.id,
                      "ref":self.name + ' - '+ self.ajuan_id.name,
                      "date":self.date,
                      "narration" : self.notes,
                      "company_id":self.company_id.id,
                      "line_ids":account_move_line,}

                journal_entry = self.env['account.move'].create(data)
                if journal_entry:
                    journal_entry.post()
                    self.write_state_line('done')
                    self.ajuan_id.write({'selesai':True})
                    self.post_mesages_uudp('Done')
                    return self.write({'state' : 'done', 'journal_entry_id':journal_entry.id})
                else:
                    raise AccessError(_('Gagal membuat journal entry') )
                return self.write({'state' : 'done'})

        if self.type == 'reimberse':
                journal_id = self.ajuan_id.pencairan_id.journal_id
                if not journal_id :
                    journal_id = self.env['account.move'].sudo().search([('ref','ilike','%'+self.ajuan_id.name+'%')],limit=1)
                    if not journal_id :
                        raise AccessError(_('Journal pencairan tidak ditemukan !'))
                    journal_id = journal_id.journal_id
                data={"journal_id":journal_id.id,
                      "ref":self.name + ' - '+ self.ajuan_id.name,
                      "date":self.date,
                      "narration" : self.notes,
                      "company_id":self.company_id.id,
                      "line_ids":account_move_line,}

                journal_entry = self.env['account.move'].create(data)
                if journal_entry:
                    journal_entry.post()
                    self.write_state_line('done')
                    self.ajuan_id.write({'selesai':True})
                    self.post_mesages_uudp('Done')
                    return self.write({'state' : 'done', 'journal_entry_id':journal_entry.id})
                else:
                    raise AccessError(_('Gagal membuat journal entry') )
                return self.write({'state' : 'done'})

        if self.type == 'pengajuan':
                journal_id = self.ajuan_id.pencairan_id.journal_id
                if not journal_id :
                    journal_id = self.env['account.move'].sudo().search([('ref','ilike','%'+self.ajuan_id.name+'%')],limit=1)
                    if not journal_id :
                        raise AccessError(_('Journal pencairan tidak ditemukan !'))
                    journal_id = journal_id.journal_id
                data={"journal_id":journal_id.id,
                      "ref":self.name + ' - '+ self.ajuan_id.name,
                      "date":self.date,
                      "narration" : self.notes,
                      "company_id":self.company_id.id,
                      "line_ids":account_move_line,}

                journal_entry = self.env['account.move'].create(data)
                if journal_entry:
                    journal_entry.post()
                    self.write_state_line('done')
                    self.ajuan_id.write({'selesai':True})
                    self.post_mesages_uudp('Done')
                    return self.write({'state' : 'done', 'journal_entry_id':journal_entry.id})
                else:
                    raise AccessError(_('Gagal membuat journal entry') )
                return self.write({'state' : 'done'})

        if self.type_pencairan == 'once':
                journal_id = self.ajuan_id.pencairan_id.journal_id
                if not journal_id :
                    journal_id = self.env['account.move'].sudo().search([('ref','ilike','%'+self.ajuan_id.name+'%')],limit=1)
                    if not journal_id :
                        raise AccessError(_('Journal pencairan tidak ditemukan !'))
                    journal_id = journal_id.journal_id
                data={"journal_id":journal_id.id,
                      "ref":self.name + ' - '+ self.ajuan_id.name,
                      "date":self.date,
                      "narration" : self.notes,
                      "company_id":self.company_id.id,
                      "line_ids":account_move_line,}

                journal_entry = self.env['account.move'].create(data)
                if journal_entry:
                    journal_entry.post()
                    self.write_state_line('done')
                    self.ajuan_id.write({'selesai':True})
                    self.post_mesages_uudp('Done')
                    return self.write({'state' : 'done', 'journal_entry_id':journal_entry.id})
                else:
                    raise AccessError(_('Gagal membuat journal entry') )
                return self.write({'state' : 'done'})


uudp()


class uudpDetail(models.Model):
    _name = "uudp.detail"
    _inherit = 'uudp.detail'

    tax_reimberse = fields.Many2many('account.tax','reimberse_tax','account_id','tax_id',string='Taxes')
    tax_amount = fields.Float(string="Amount Tax", compute="_calc_sub_total", store=True)
    
    @api.depends('qty','unit_price','state','tax_reimberse')
    def _calc_sub_total(self):
        for x in self:
            qty = x.qty
            price = x.unit_price
            sub_total = qty * price
            tax_reimberse = x.tax_reimberse.amount
            tax_amount = sub_total*tax_reimberse/100
            x.tax_amount = tax_amount
            x.sub_total = sub_total-tax_amount
            x.total = sub_total

uudpDetail()

class uudpPencairan(models.Model):
    _name = 'uudp.pencairan'
    _inherit = 'uudp.pencairan'

    reviewed_by = fields.Many2one(comodel_name='hr.employee',string='Reviewed by')
    budgeted_by = fields.Many2one(comodel_name='hr.employee',string='Budget Confirmed')
    approved_by = fields.Many2one(comodel_name='hr.employee',string='Approved by')


    @api.multi
    def button_done_once(self):
        self.ensure_one()
        total_ajuan = 0
        now = datetime.datetime.now()
        if self.uudp_ids:
            for ajuan in self.uudp_ids:
                tgl_pencairan = self.tgl_pencairan
                if ajuan.tgl_pencairan :
                    tgl_pencairan = ajuan.tgl_pencairan
                #  tansfer tidak langsung create jurnal
                if ajuan.cara_bayar == 'transfer' :
                    datas = {'total_pencairan'          : ajuan.total_ajuan,
                                'state'                 : 'confirm_accounting',
                                'pencairan_id'          : self.id,
                                'tgl_pencairan'         : tgl_pencairan,
                                'terbilang'             : terbilang.terbilang(int(round(ajuan.total_ajuan,0)), "IDR", "id"),}
                    ajuan.write(datas)
                    continue 
                account_move = self.env['account.move']
                reference =  self.name + ' - ' + ajuan.name
                account_move_line = []
                total_kredit = 0
                # not_confirmed_accounting = ajuan.uudp_ids.filtered(lambda x: x.state != 'confirm_accounting')
                # if not_confirmed_accounting :
                #     raise AccessError(_('Ada ajuan yang belum confirm accounting !') )
                partner = ajuan.responsible_id.partner_id.id
                for juan in ajuan.uudp_ids :
                    if juan.partner_id :
                        partner = juan.partner_id.id
                    tag_id = False
                    if juan.store_id and juan.store_id.account_analytic_tag_id :
                        tag_id = [(6, 0, [juan.store_id.account_analytic_tag_id.id])]
                    if ajuan.type == 'pengajuan' :
                        debit = ajuan.coa_debit
                        if not debit :
                            raise AccessError(_('Debit acount pada ajuan %s belum diisi !') % (ajuan.name) )
                    else :
                        debit = juan.coa_debit
                        if not debit :
                            raise AccessError(_('Debit Account lines pada ajuan %s belum diisi !') % (ajuan.name) )
                    #account debit
                    if juan.total > 0.0 :
                        account_move_line.append((0, 0 ,{'account_id'       : debit.id,
                                                        'partner_id'        : partner,
                                                        'analytic_account_id' : ajuan.department_id.analytic_account_id.id or False,
                                                        'analytic_tag_ids'  : tag_id,
                                                        'name'              : juan.description,
                                                        'debit'             : juan.total,
                                                        'date'              : tgl_pencairan,
                                                        'date_maturity'     : tgl_pencairan}))
                    elif juan.total < 0.0 :
                        account_move_line.append((0, 0 ,{'account_id'       : debit.id,
                                                        'partner_id'        : partner,
                                                        'analytic_account_id' : ajuan.department_id.analytic_account_id.id or False,
                                                        'analytic_tag_ids'  : tag_id,
                                                        'name'              : juan.description,
                                                        'credit'             : -juan.total,
                                                        'date'              : tgl_pencairan,
                                                        'date_maturity'     : tgl_pencairan}))
                #account credit bank / hutang
                notes = ajuan.notes
                if not notes :
                    notes= self.coa_kredit.name
                account_move_line.append((0, 0 ,{'account_id'       : self.coa_kredit.id,
                                                'partner_id'        : ajuan.responsible_id.partner_id.id,
                                                'analytic_account_id' : ajuan.department_id.analytic_account_id.id or False,
                                                'name'              : notes,
                                                'credit'            : ajuan.total_ajuan,
                                                'date'              : tgl_pencairan,
                                                'date_maturity'     : tgl_pencairan}))

                journal_id = ajuan.pencairan_id.journal_id
                if not journal_id :
                    journal_id = self.env['account.move'].sudo().search([('ref','ilike','%'+ajuan.name+'%')],limit=1)
                    if not journal_id :
                        raise AccessError(_('Journal pencairan tidak ditemukan !'))
                    journal_id = journal_id.journal_id
                data={"journal_id"  : self.journal_id.id,
                      "ref"         : self.name + ' - ' + ajuan.name,
                      "date"        : tgl_pencairan,
                      "company_id"  : self.company_id.id,
                      "narration"   : self.notes,
                      "terbilang"   : terbilang.terbilang(int(round(ajuan.total_ajuan,0)), "IDR", "id"),
                      "line_ids"    : account_move_line,}

                journal_entry = self.env['account.move'].create(data)
                if journal_entry:
                    journal_entry.post()
                    # self.write_state_line('done')
                    ajuan.write({'selesai':True})
                    self.post_mesages_pencairan('Done')
                    return self.write({'state' : 'done', 'journal_entry_id':journal_entry.id})
                else:
                    raise AccessError(_('Gagal membuat journal entry') )
                return self.write({'state' : 'done'})

uudpPencairan()