# -*- coding: utf-8 -*-
from odoo import http

# class VitReportBillplanFixer(http.Controller):
#     @http.route('/vit_report_billplan_fixer/vit_report_billplan_fixer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_report_billplan_fixer/vit_report_billplan_fixer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_report_billplan_fixer.listing', {
#             'root': '/vit_report_billplan_fixer/vit_report_billplan_fixer',
#             'objects': http.request.env['vit_report_billplan_fixer.vit_report_billplan_fixer'].search([]),
#         })

#     @http.route('/vit_report_billplan_fixer/vit_report_billplan_fixer/objects/<model("vit_report_billplan_fixer.vit_report_billplan_fixer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_report_billplan_fixer.object', {
#             'object': obj
#         })