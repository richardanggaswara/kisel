# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

STATES = [('open','Open'), ('baut','BAUT'), ('bast','BAST'), ('close','Close'), ('cancel','Cancel')]

class bill_plan(models.Model):
    _inherit = 'vit_project_billplan.bill_plan'
    
    no_bast = fields.Char(string="Nomor BAST", states={'bast': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'baut': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
    no_baut = fields.Char(string="Nomor BAUT", states={'baut': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'bast': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
    bast_date = fields.Date( string="BAST Date", help="", states={'bast': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'baut': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
    baut_date = fields.Date( string="BAUT Date", help="", states={'baut': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'bast': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
    description = fields.Text(string="Deskripsi Fase")
    state = fields.Selection(string="State", selection=STATES,required=True, readonly=True, default=STATES[0][0])

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