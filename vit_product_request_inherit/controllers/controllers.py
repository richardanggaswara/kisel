# -*- coding: utf-8 -*-
from odoo import http

# class VitProductRequestInherit(http.Controller):
#     @http.route('/vit_product_request_inherit/vit_product_request_inherit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_product_request_inherit/vit_product_request_inherit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_product_request_inherit.listing', {
#             'root': '/vit_product_request_inherit/vit_product_request_inherit',
#             'objects': http.request.env['vit_product_request_inherit.vit_product_request_inherit'].search([]),
#         })

#     @http.route('/vit_product_request_inherit/vit_product_request_inherit/objects/<model("vit_product_request_inherit.vit_product_request_inherit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_product_request_inherit.object', {
#             'object': obj
#         })