# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import xlwt
from xlsxwriter.workbook import Workbook
from io import StringIO
import base64
import time
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

STATES = [('draft','Draft'),('done', 'Done'), ('cancel', 'Cancel')]

class vit_report_aging_muka(models.Model):
    _name = 'vitreport.agingmuka'
    
    notes = fields.Text(string="Notes")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    state = fields.Selection(string="State", selection=STATES, required=True, readonly=True, default=STATES[0][0])
    date_to = fields.Date(string='End Date')
    date_from = fields.Date(string="Date", required=True)
    # period_length = fields.Integer(string="Period Length(days)", required=True)
    coa_debit = fields.Many2one("account.account", string="Account",required=True)
    
    @api.multi
    def action_draft(self):
        self.write({'state': STATES[0][0]})

    @api.multi
    def action_done(self):
        self.write({'state': STATES[1][0]})

    @api.multi
    def action_cancel(self):
        self.write({'state' : STATES[2][0]})

    @api.multi
    def print_report_aging(self):
        today = datetime.datetime(2020, 3, 5)
        today = str(today)
        get_day = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S").day
        print(get_day)
        self.env.ref('vit_report_aging_muka.report_aging_muka').report_action(self)