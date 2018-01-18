# -*- coding: utf-8 -*-
from odoo import http

# class OldId(http.Controller):
#     @http.route('/old_id/old_id/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/old_id/old_id/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('old_id.listing', {
#             'root': '/old_id/old_id',
#             'objects': http.request.env['old_id.old_id'].search([]),
#         })

#     @http.route('/old_id/old_id/objects/<model("old_id.old_id"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('old_id.object', {
#             'object': obj
#         })