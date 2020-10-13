# -*- coding: utf-8 -*-
from odoo import http

# class VitProductRequestHideVendor(http.Controller):
#     @http.route('/vit_product_request_hide_vendor/vit_product_request_hide_vendor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_product_request_hide_vendor/vit_product_request_hide_vendor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_product_request_hide_vendor.listing', {
#             'root': '/vit_product_request_hide_vendor/vit_product_request_hide_vendor',
#             'objects': http.request.env['vit_product_request_hide_vendor.vit_product_request_hide_vendor'].search([]),
#         })

#     @http.route('/vit_product_request_hide_vendor/vit_product_request_hide_vendor/objects/<model("vit_product_request_hide_vendor.vit_product_request_hide_vendor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_product_request_hide_vendor.object', {
#             'object': obj
#         })