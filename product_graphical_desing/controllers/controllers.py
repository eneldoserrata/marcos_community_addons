# -*- coding: utf-8 -*-
from openerp import http

# class ProductGraphicalDesing(http.Controller):
#     @http.route('/product_graphical_desing/product_graphical_desing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_graphical_desing/product_graphical_desing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_graphical_desing.listing', {
#             'root': '/product_graphical_desing/product_graphical_desing',
#             'objects': http.request.env['product_graphical_desing.product_graphical_desing'].search([]),
#         })

#     @http.route('/product_graphical_desing/product_graphical_desing/objects/<model("product_graphical_desing.product_graphical_desing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_graphical_desing.object', {
#             'object': obj
#         })