# -*- coding: utf-8 -*-
from openerp import http

# class CurrencyCheck(http.Controller):
#     @http.route('/currency_check/currency_check/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/currency_check/currency_check/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('currency_check.listing', {
#             'root': '/currency_check/currency_check',
#             'objects': http.request.env['currency_check.currency_check'].search([]),
#         })

#     @http.route('/currency_check/currency_check/objects/<model("currency_check.currency_check"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('currency_check.object', {
#             'object': obj
#         })