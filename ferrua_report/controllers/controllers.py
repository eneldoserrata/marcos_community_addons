# -*- coding: utf-8 -*-
from openerp import http

# class FerruaReport(http.Controller):
#     @http.route('/ferrua_report/ferrua_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ferrua_report/ferrua_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ferrua_report.listing', {
#             'root': '/ferrua_report/ferrua_report',
#             'objects': http.request.env['ferrua_report.ferrua_report'].search([]),
#         })

#     @http.route('/ferrua_report/ferrua_report/objects/<model("ferrua_report.ferrua_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ferrua_report.object', {
#             'object': obj
#         })