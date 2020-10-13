from odoo import models, fields, api, _
import time
from io import BytesIO
import xlsxwriter
import base64
from odoo.exceptions import Warning
import logging
from datetime import datetime, timedelta
_logger = logging.getLogger(__name__)

class export_excel_wizard(models.TransientModel):
	_name = 'vit.bill_plan'

# class bill_plan(models.Model):
# 	_inherit = "vit_project_billplan.bill_plan"

	# export_file = fields.Binary(string="Export File",  )
	# export_filename = fields.Char(string="Export File",  )

	def cell_format(self, workbook):
		cell_format = {}
		cell_format['title'] = workbook.add_format({
			'bold': True,
			'align': 'center',
			'valign': 'vcenter',
			'font_size': 20,
			'font_name': 'Arial',
		})
		cell_format['header'] = workbook.add_format({
			'bold': True,
			'align': 'center',
			'border': True,
			'font_name': 'Arial',
		})
		cell_format['content'] = workbook.add_format({
			'font_size': 11,
			'border': False,
			'font_name': 'Arial',
		})
		cell_format['content_float'] = workbook.add_format({
			'font_size': 11,
			'border': True,
			'num_format': '#,##0.00',
			'font_name': 'Arial',
		})
		cell_format['total'] = workbook.add_format({
			'bold': True,
			'num_format': '#,##0.00',
			'border': True,
			'font_name': 'Arial',
		})
		return cell_format, workbook
	data = fields.Binary('File')

	@api.multi
	def export_excel(self):
		headers = [
			"No.", "ID Project", "Tanggal Periode",
			"Unit", "Wilayah", "Bisnis", "Jenis Project", "Customer",
			# "Afiliasi",
			"Nomor Billplan", "Reference", "Tanggal Billplan", 
			"Rencana Penagihan", "Description Fase", "Nilai Revenue", 
			"Nilai ID Project", "Sisa ID Project", "Nomor BAUT", 
			"Tanggal BAUT", "Nomor BAST", "Tanggal BAST", 
			"Status Fase", "Umur Billplan(Days)",
			]

		fp = BytesIO()
		workbook = xlsxwriter.Workbook(fp)
		cell_format, workbook = self.cell_format(workbook)
		worksheet = workbook.add_worksheet()
		worksheet.set_column('A:ZZ', 30)
		column_length = len(headers)
		worksheet.write(0, 4, "REPORT BILLPLAN")
		billplan_ids = self.env['vit_project_billplan.bill_plan'].search([])
		column = 0
		row = 4
		for col in headers:
			worksheet.write(row, column, col, cell_format['header'])
			column += 1
		row = 5
		final_data=[]
		no=1
		for data in billplan_ids :
			date_1 = datetime.strftime(data.date, '%d-%m-%Y') if data.date else ''	
			plan_date_1 = datetime.strftime(data.plan_date, '%d-%m-%Y') if data.plan_date else ''	
			baut_date_1 = datetime.strftime(data.baut_date, '%d-%m-%Y') if data.baut_date else ''
			bast_date_1 = datetime.strftime(data.bast_date, '%d-%m-%Y') if data.bast_date else ''	
			# if "Telkomsel" == data.project_id.partner_id.name or "TELKOMSEL" == data.project_id.partner_id.name : 
			# 	dataproject = "Telkomsel"
			# else:
			# 	dataproject = "Non Telkomsel"
			if data.state == 'open':
				status = "Fase 1"
				stat = "BAST belum selesai"
			if data.state == 'baut':
				status = "Fase 2"
				stat = "BAST belum selesai"
			if data.state == 'bast':
				status = "Fase 3"
				stat = "BAST belum selesai"
			if data.state == 'close':
				status = "Fase 3"
				bast_date_2 = str(bast_date_1) 
				date_2 = str(date_1)
				start = datetime.strptime(bast_date_2, '%d-%m-%Y')
				sub = datetime.strptime(date_2, '%d-%m-%Y')
				stat = start-sub
			final_data.append([
				no,
				data.analytic_account_id.name,
				date_1,
				data.unit_id.name,
				data.analytic_tag_ids.name,
				data.analytic_tag_ids_b.name,
				data.project_id.project_type_id.name,
				data.project_id.partner_id.name,
				# dataproject,
				data.name,
				data.reference,
				date_1,
				plan_date_1,
				data.description,
				'{0:,.2f}'.format(data.amount),
				'{0:,.2f}'.format(data.project_id.total_revenue),
				'{0:,.2f}'.format(data.project_id.total_revenue - data.amount),
				data.no_baut,
				baut_date_1,
				data.no_bast,
				bast_date_1,
				status,
				stat,
			])
			no += 1
		for data in final_data:
			column = 0
			for col in data:
				worksheet.write(row, column, col, cell_format['content'] if column<2 else  cell_format['content_float'])
				column += 1
			row += 1

		workbook.close()
		result = base64.encodestring(fp.getvalue())
		filename = 'ReportBillplan'+'%2Exlsx'
		self.write({'data':result})
		url = "web/content/?model="+self._name+"&id="+str(self.id)+"&field=data&download=true&filename="+filename
		return {
			'type': 'ir.actions.act_url',
			'url': url,
			'target': 'new',
		}