# -*- coding: utf-8 -*-
from openerp import http

# class L10nDoPostalCode(http.Controller):
#     @http.route('/l10n_do_postal_code/l10n_do_postal_code/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_do_postal_code/l10n_do_postal_code/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_do_postal_code.listing', {
#             'root': '/l10n_do_postal_code/l10n_do_postal_code',
#             'objects': http.request.env['l10n_do_postal_code.l10n_do_postal_code'].search([]),
#         })

#     @http.route('/l10n_do_postal_code/l10n_do_postal_code/objects/<model("l10n_do_postal_code.l10n_do_postal_code"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_do_postal_code.object', {
#             'object': obj
#         })