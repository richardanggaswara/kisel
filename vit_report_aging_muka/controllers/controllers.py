# -*- coding: utf-8 -*-
from odoo import http

# class VitReportAgingMuka(http.Controller):
#     @http.route('/vit_report_aging_muka/vit_report_aging_muka/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_report_aging_muka/vit_report_aging_muka/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_report_aging_muka.listing', {
#             'root': '/vit_report_aging_muka/vit_report_aging_muka',
#             'objects': http.request.env['vit_report_aging_muka.vit_report_aging_muka'].search([]),
#         })

#     @http.route('/vit_report_aging_muka/vit_report_aging_muka/objects/<model("vit_report_aging_muka.vit_report_aging_muka"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_report_aging_muka.object', {
#             'object': obj
#         })