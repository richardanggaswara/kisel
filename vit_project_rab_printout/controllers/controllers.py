# -*- coding: utf-8 -*-
from odoo import http

# class VitProjectRabPrintout(http.Controller):
#     @http.route('/vit_project_rab_printout/vit_project_rab_printout/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_project_rab_printout/vit_project_rab_printout/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_project_rab_printout.listing', {
#             'root': '/vit_project_rab_printout/vit_project_rab_printout',
#             'objects': http.request.env['vit_project_rab_printout.vit_project_rab_printout'].search([]),
#         })

#     @http.route('/vit_project_rab_printout/vit_project_rab_printout/objects/<model("vit_project_rab_printout.vit_project_rab_printout"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_project_rab_printout.object', {
#             'object': obj
#         })