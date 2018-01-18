# -*- coding: utf-8 -*-
from odoo import http

# class ArodooStockBarcode(http.Controller):
#     @http.route('/arodoo_stock_barcode/arodoo_stock_barcode/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/arodoo_stock_barcode/arodoo_stock_barcode/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('arodoo_stock_barcode.listing', {
#             'root': '/arodoo_stock_barcode/arodoo_stock_barcode',
#             'objects': http.request.env['arodoo_stock_barcode.arodoo_stock_barcode'].search([]),
#         })

#     @http.route('/arodoo_stock_barcode/arodoo_stock_barcode/objects/<model("arodoo_stock_barcode.arodoo_stock_barcode"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('arodoo_stock_barcode.object', {
#             'object': obj
#         })