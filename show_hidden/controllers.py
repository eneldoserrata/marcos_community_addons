# -*- coding: utf-8 -*-
from openerp import http

# class ShowHidden(http.Controller):
#     @http.route('/show_hidden/show_hidden/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/show_hidden/show_hidden/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('show_hidden.listing', {
#             'root': '/show_hidden/show_hidden',
#             'objects': http.request.env['show_hidden.show_hidden'].search([]),
#         })

#     @http.route('/show_hidden/show_hidden/objects/<model("show_hidden.show_hidden"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('show_hidden.object', {
#             'object': obj
#         })