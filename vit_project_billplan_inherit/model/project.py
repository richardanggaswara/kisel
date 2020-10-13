#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    @api.depends('billplan_ids')
    def _get_billplan_count(self):
        for rec in self:
            rec.billplan_count = len(rec.billplan_ids)

    billplan_count = fields.Integer( string="Billplan count",  help="", compute="_get_billplan_count")
    billplan_ids = fields.One2many(comodel_name="vit_project_billplan.bill_plan",  inverse_name="project_id",  string="Billplans",  help="")

    @api.multi
    def action_view_billplan(self):
        '''
        This function returns an action that display existing BAKN of given purchase order ids.
        When only one found, show the BAKN immediately.
        '''
        action = self.env.ref('vit_project_billplan.action_vit_project_billplan_bill_plan')
        result = action.read()[0]
        # create_bill = self.env.context.get('create_bill', False)
        # override the context to get rid of the default filtering
        result['context'] = {
            # 'type': 'in_invoice',
            'default_project_id': self.id,
            'default_analytic_account_id':self.analytic_account_id.id,
            'default_currency_id': self.currency_id.id,
            'default_company_id': self.company_id.id,
            'company_id': self.company_id.id
        }
        # choose the view_mode accordingly
        if len(self.billplan_ids) > 1 :
            result['domain'] = "[('id', 'in', " + str(self.billplan_ids.ids) + ")]"
        else:
            res = self.env.ref('vit_project_billplan.view_vit_project_billplan_bill_plan_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            # Do not set an invoice_id if we want to create a new bill.
            # if not create_bill:
            result['res_id'] = self.billplan_ids.id or False
        return result