# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vit_rpqpo(models.Model):
	_name = 'purchase.order.line'
	_inherit = 'purchase.order.line'

	account_analytic_id = fields.Many2one('account.analytic.account', string='Unit')
	lokasi = fields.Many2one(comodel_name='account.analytic.tag',
										string='Location', 
										domain=[('analytic_dimension_id.name','=','LOCATION')]
										)
	bisniss = fields.Many2one(comodel_name='account.analytic.tag', 
							string='Business', 
							domain=[('analytic_dimension_id.name','=','BUSINESS')]
							)