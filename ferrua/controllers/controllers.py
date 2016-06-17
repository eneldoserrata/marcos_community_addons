# -*- coding: utf-8 -*-
from openerp import http

# class ProductNameComposer(http.Controller):
#     @http.route('/product_name_composer/product_name_composer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_name_composer/product_name_composer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_name_composer.listing', {
#             'root': '/product_name_composer/product_name_composer',
#             'objects': http.request.env['product_name_composer.product_name_composer'].search([]),
#         })

#     @http.route('/product_name_composer/product_name_composer/objects/<model("product_name_composer.product_name_composer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_name_composer.object', {
#             'object': obj
#         })