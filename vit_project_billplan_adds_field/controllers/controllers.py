# -*- coding: utf-8 -*-
from odoo import http

# class VitProjectBillplanAddsField(http.Controller):
#     @http.route('/vit_project_billplan_adds_field/vit_project_billplan_adds_field/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_project_billplan_adds_field/vit_project_billplan_adds_field/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_project_billplan_adds_field.listing', {
#             'root': '/vit_project_billplan_adds_field/vit_project_billplan_adds_field',
#             'objects': http.request.env['vit_project_billplan_adds_field.vit_project_billplan_adds_field'].search([]),
#         })

#     @http.route('/vit_project_billplan_adds_field/vit_project_billplan_adds_field/objects/<model("vit_project_billplan_adds_field.vit_project_billplan_adds_field"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_project_billplan_adds_field.object', {
#             'object': obj
#         })