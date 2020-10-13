#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
# from io import BytesIO
# import xlsxwriter
# import base64
from odoo.exceptions import Warning
import logging
from datetime import datetime, timedelta
_logger = logging.getLogger(__name__)


STATES = [('open','Open'), ('baut','BAUT'), ('bast','BAST'), ('close','Close'), ('cancel','Cancel')]

class bill_plan(models.Model):
	_inherit = "vit_project_billplan.bill_plan"

	no_bast = fields.Char(string="Nomor BAST", states={'bast': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'baut': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	no_baut = fields.Char(string="Nomor BAUT", states={'baut': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'bast': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	bast_date = fields.Date( string="BAST Date", help="", states={'bast': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'baut': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	baut_date = fields.Date( string="BAUT Date", help="", states={'baut': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'bast': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	description = fields.Text(string="Deskripsi Fase")
	state = fields.Selection(string="State", selection=STATES, required=True, readonly=True, default=STATES[0][0])
	# billplan_ids = fields.One2many('vit_project_billplan.bill_plan','project_id',string="Billplan")

	@api.multi
	def action_baut(self):
		self.write({'state': STATES[1][0]})
	@api.multi
	def action_bast(self):
		self.write({'state': STATES[2][0]})
	@api.multi
	def action_close(self):
		self.write({'state': STATES[3][0]})
	@api.multi
	def action_cancel(self):
		self.write({'state': STATES[4][0]})

	# def cell_format(self, workbook):
	# 	cell_format = {}
	# 	cell_format['title'] = workbook.add_format({
	# 		'bold': True,
	# 		'align': 'center',
	# 		'valign': 'vcenter',
	# 		'font_size': 20,
	# 		'font_name': 'Arial',
	# 	})
	# 	cell_format['header'] = workbook.add_format({
	# 		'bold': True,
	# 		'align': 'center',
	# 		'border': True,
	# 		'font_name': 'Arial',
	# 	})
	# 	cell_format['content'] = workbook.add_format({
	# 		'font_size': 11,
	# 		'border': False,
	# 		'font_name': 'Arial',
	# 	})
	# 	cell_format['content_float'] = workbook.add_format({
	# 		'font_size': 11,
	# 		'border': True,
	# 		'num_format': '#,##0.00',
	# 		'font_name': 'Arial',
	# 	})
	# 	cell_format['total'] = workbook.add_format({
	# 		'bold': True,
	# 		'num_format': '#,##0.00',
	# 		'border': True,
	# 		'font_name': 'Arial',
	# 	})
	# 	return cell_format, workbook
	# data = fields.Binary('File')

	# @api.multi
	# def export_excel(self):
	# 	headers = [
	# 		"No.", "ID Project", "Tanggal Periode",
	# 		"Unit", "Wilayah", "Bisnis", "Jenis Project", "Customer",
	# 		# "Afiliasi",
	# 		"Nomor Billplan", "Reference", "Tanggal Billplan", 
	# 		"Rencana Penagihan", "Description Fase", "Nilai Revenue", 
	# 		"Nilai ID Project", "Sisa ID Project", "Nomor BAUT", 
	# 		"Tanggal BAUT", "Nomor BAST", "Tanggal BAST", 
	# 		"Status Fase", "Umur Billplan(Days)",
	# 		]

	# 	fp = BytesIO()
	# 	workbook = xlsxwriter.Workbook(fp)
	# 	cell_format, workbook = self.cell_format(workbook)
	# 	worksheet = workbook.add_worksheet()
	# 	worksheet.set_column('A:ZZ', 30)
	# 	column_length = len(headers)
	# 	worksheet.write(0, 4, "REPORT BILLPLAN")
	# 	billplan_ids = self.env['vit_project_billplan.bill_plan'].search([])
	# 	column = 0
	# 	row = 4
	# 	for col in headers:
	# 		worksheet.write(row, column, col, cell_format['header'])
	# 		column += 1
	# 	row = 5
	# 	final_data=[]
	# 	no=1
	# 	for data in billplan_ids :
	# 		date_1 = datetime.strftime(data.date, '%d-%m-%Y') if data.date else ''	
	# 		plan_date_1 = datetime.strftime(data.plan_date, '%d-%m-%Y') if data.plan_date else ''	
	# 		baut_date_1 = datetime.strftime(data.baut_date, '%d-%m-%Y') if data.baut_date else ''
	# 		bast_date_1 = datetime.strftime(data.bast_date, '%d-%m-%Y') if data.bast_date else ''	
	# 		# if "Telkomsel" == data.project_id.partner_id.name or "TELKOMSEL" == data.project_id.partner_id.name : 
	# 		# 	dataproject = "Telkomsel"
	# 		# else:
	# 		# 	dataproject = "Non Telkomsel"
	# 		if data.state == 'open':
	# 			status = "Fase 1"
	# 			stat = "BAST belum selesai"
	# 		if data.state == 'baut':
	# 			status = "Fase 2"
	# 			stat = "BAST belum selesai"
	# 		if data.state == 'bast':
	# 			status = "Fase 3"
	# 			stat = "BAST belum selesai"
	# 		if data.state == 'close':
	# 			status = "Fase 3"
	# 			bast_date_2 = str(bast_date_1) 
	# 			date_2 = str(date_1)
	# 			start = datetime.strptime(bast_date_2, '%d-%m-%Y')
	# 			sub = datetime.strptime(date_2, '%d-%m-%Y')
	# 			stat = start-sub
	# 		final_data.append([
	# 			no,
	# 			data.analytic_account_id.name,
	# 			date_1,
	# 			data.unit_id.name,
	# 			data.analytic_tag_ids.name,
	# 			data.analytic_tag_ids_b.name,
	# 			data.project_id.project_type_id.name,
	# 			data.project_id.partner_id.name,
	# 			# dataproject,
	# 			data.name,
	# 			data.reference,
	# 			date_1,
	# 			plan_date_1,
	# 			data.description,
	# 			'{0:,.2f}'.format(data.amount),
	# 			'{0:,.2f}'.format(data.project_id.total_revenue),
	# 			'{0:,.2f}'.format(data.project_id.total_revenue - data.amount),
	# 			data.no_baut,
	# 			baut_date_1,
	# 			data.no_bast,
	# 			bast_date_1,
	# 			status,
	# 			stat,
	# 		])
	# 		no += 1
	# 	for data in final_data:
	# 		column = 0
	# 		for col in data:
	# 			worksheet.write(row, column, col, cell_format['content'] if column<2 else  cell_format['content_float'])
	# 			column += 1
	# 		row += 1

	# 	workbook.close()
	# 	result = base64.encodestring(fp.getvalue())
	# 	filename = 'ReportBillplan'+'%2Exlsx'
	# 	self.write({'data':result})
	# 	url = "web/content/?model="+self._name+"&id="+str(self.id)+"&field=data&download=true&filename="+filename
	# 	return {
	# 		'type': 'ir.actions.act_url',
	# 		'url': url,
	# 		'target': 'new',
	# 	}

class bill_plan(models.Model):
	_inherit = "vit_project_billplan.bill_plan"

	name = fields.Char( required=False, readonly=True, string="Name",  help="")
	amount = fields.Float( compute="_calc_total", string="Amount",  help="")
	
	@api.depends('amount','line_ids')
	def _calc_total(self):
		am_total = 0.0
		for amou in self:
			for am in amou.line_ids:
				am_total += am.amount
				amou.amount = am_total

	@api.model
	def create(self, vals):
		vals['name']    = self.env['ir.sequence'].next_by_code('billplan.code')
		new_billplan = super(bill_plan, self).create(vals)
		new_billplan.fill_product()
		return new_billplan

	@api.multi
	def action_create_so(self):
		so_obj = self.env['sale.order']

		order_line = []

		for line in self.line_ids:
			if not line.product_id:
				raise Warning('Product di Project Revenue kosong!')
			order_line.append((0,0,{
				'analytic_account_id': line.bill_plan_id.analytic_account_id.id,
				'unit_id': line.bill_plan_id.unit_id.id,
				'analytic_tag_ids_l': line.bill_plan_id.analytic_tag_ids.id,
				'analytic_tag_ids_b': line.bill_plan_id.analytic_tag_ids_b.id,
				'product_id': line.product_id.id,
				'name':line.name,
				'product_uom_qty': line.quantity,
				'price_unit': line.amount
			}))

		so_obj.create({
			'partner_id': self.project_id.partner_id.id ,
			'date_order': fields.Datetime.now(),
			'billplan_id': self.id,
			'order_line': order_line
		})

	@api.depends('sale_ids')
	def _get_sale_count(self):
		for rec in self:
			rec.sale_count = len(rec.sale_ids)


	sale_count = fields.Integer( string="SO count",  help="", compute="_get_sale_count")
	sale_ids = fields.One2many(comodel_name="sale.order",  inverse_name="billplan_id",  string="SO(s)",  help="")


	@api.multi
	def action_view_sale(self):

		action = self.env.ref('sale.action_orders')
		result = action.read()[0]

		result['context'] = {
			'default_billplan_id': self.id,
			'default_partner_id': self.project_id.partner_id.id,
			# 'default_company_id': self.company_id.id,
			# 'company_id': self.company_id.id
		}
		# choose the view_mode accordingly
		if len(self.sale_ids) > 1 :
			result['domain'] = "[('id', 'in', " + str(self.sale_ids.ids) + ")]"
		else:
			res = self.env.ref('sale.view_order_form', False)
			result['views'] = [(res and res.id or False, 'form')]
			result['res_id'] = self.sale_ids.id or False
		return result

	line_ids = fields.One2many(comodel_name="vit_project_billplan.bill_plan_line", inverse_name="bill_plan_id", string="Line", required=False, )


	@api.multi
	def fill_product(self):
		lines = []
		sql = "delete from vit_project_billplan_bill_plan_line where bill_plan_id=%s"
		self.env.cr.execute(sql, (self.id,))
		# import pdb;pdb.set_trace()
		for project in self.project_id:
			for rev in project.revenue_ids:
				if not rev.product:
					raise Warning('Product di Project Revenue kosong!')
				total_qty = rev.quantity
				# bill_plan = self.search([('project_id','=',rev.name)])
				data_line = self.line_ids.search([('product_id','=',rev.product.id)])
				for x in data_line:
					if x.quantity != rev.quantity and x.unit_price == rev.amount and x.name == rev.name:
						total_qty -= x.quantity
					if total_qty < 1:
						raise Warning('Quantity Pada Product Kosong!')
				lines.append( (0,0,{
						'name'      : rev.name,
						'product_id': rev.product.id,
						'quantity'  : total_qty,
						'unit_price': rev.amount,
						'amount'    : rev.amount_total,
					}) )
		print(lines)

		self.line_ids = lines

class billplan_line(models.Model):
	_name = 'vit_project_billplan.bill_plan_line'

	name            = fields.Char(string="Name", required=False, )
	bill_plan_id    = fields.Many2one(comodel_name="vit_project_billplan.bill_plan", string="Bill Plan", required=False, )
	product_id      = fields.Many2one(comodel_name="product.product", string="Product", required=False, )
	quantity        = fields.Float(string="Quantity",  required=False, )
	amount          = fields.Float(compute="_calc_total", string="Amount",  required=False, )
	unit_price      = fields.Float( string="Unit Price",  help="")

	@api.depends('quantity','unit_price')
	def _calc_total(self):
		for rec in self:
			rec.amount = rec.quantity * rec.unit_price
