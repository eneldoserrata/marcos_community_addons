# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013-2015 Marcos Organizador de Negocios SRL http://marcos.do
#    Write by Eneldo Serrata (eneldo@marcos.do)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import http

class L10nDoHrPayroll(http.Controller):
    @http.route('/l10n_do_hr_payroll/l10n_do_hr_payroll/', auth='public')
    def index(self, **kw):
        return "Hello, world"
#
    @http.route('/l10n_do_hr_payroll/l10n_do_hr_payroll/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('l10n_do_hr_payroll.listing', {
            'root': '/l10n_do_hr_payroll/l10n_do_hr_payroll',
            'objects': http.request.env['l10n_do_hr_payroll.l10n_do_hr_payroll'].search([]),
        })
#
    @http.route('/l10n_do_hr_payroll/l10n_do_hr_payroll/objects/<model("l10n_do_hr_payroll.l10n_do_hr_payroll"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('l10n_do_hr_payroll.object', {
            'object': obj
        })