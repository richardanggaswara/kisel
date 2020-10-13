#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class bill_plan(models.Model):

    _name = "vit_project_billplan.bill_plan"
    _inherit = ['mail.thread']

    name = fields.Char( required=True, string="Name",  help="")
    date = fields.Date( string="Date",  help="")
    plan_date = fields.Date( string="Plan date",  help="")
    baut_date = fields.Date( string="BAUT Date",  help="")
    bast_date = fields.Date( string="BAST Date",  help="")
    amount = fields.Float( string="Amount",  help="")
    reference = fields.Char( string="Reference",  help="")


    project_id = fields.Many2one(comodel_name="project.project",  string="Project",  help="")
    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account",  string="Analytic account",  help="")
    department_id = fields.Many2one(comodel_name="hr.department",  string="Department",  help="")
    lokasi_id = fields.Many2one(comodel_name="account.analytic.tag",  string="Lokasi",  help="")
    bisnis_id = fields.Many2one(comodel_name="account.analytic.tag",  string="Bisnis",  help="")