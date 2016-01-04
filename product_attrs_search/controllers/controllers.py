# -*- coding: utf-8 -*-
from openerp import http

# class ProductAttrsSearch(http.Controller):
#     @http.route('/product_attrs_search/product_attrs_search/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_attrs_search/product_attrs_search/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_attrs_search.listing', {
#             'root': '/product_attrs_search/product_attrs_search',
#             'objects': http.request.env['product_attrs_search.product_attrs_search'].search([]),
#         })

#     @http.route('/product_attrs_search/product_attrs_search/objects/<model("product_attrs_search.product_attrs_search"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_attrs_search.object', {
#             'object': obj
#         })