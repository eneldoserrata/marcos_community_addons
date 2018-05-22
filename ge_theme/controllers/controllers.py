# -*- coding: utf-8 -*-
from odoo import http

# class GeTheme(http.Controller):
#     @http.route('/ge_theme/ge_theme/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ge_theme/ge_theme/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ge_theme.listing', {
#             'root': '/ge_theme/ge_theme',
#             'objects': http.request.env['ge_theme.ge_theme'].search([]),
#         })

#     @http.route('/ge_theme/ge_theme/objects/<model("ge_theme.ge_theme"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ge_theme.object', {
#             'object': obj
#         })