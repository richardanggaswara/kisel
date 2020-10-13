#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class project(models.Model):

    _name = "project.project"

    _inherit = "project.project"
    billplan_count = fields.Integer( string="Billplan count",  help="")


    billplan_ids = fields.One2many(comodel_name="vit_project_billplan.bill_plan",  inverse_name="project_id",  string="Billplans",  help="")
