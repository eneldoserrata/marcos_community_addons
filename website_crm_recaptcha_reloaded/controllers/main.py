# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C)2004-TODAY Tech Receptives(<https://www.techreceptives.com>)
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
from openerp.addons.web import http
from openerp.addons.web.http import request
import openerp.addons.website_crm.controllers.main as main
from openerp.tools.translate import _


class contactus(main.contactus):
    
    @http.route(['/crm/contactus'], type='http', auth="public", website=True)
    def contactus(self, **kwargs):
        if kwargs.has_key('g-recaptcha-response') and request.website.is_captcha_valid(kwargs['g-recaptcha-response']):
            return super(contactus, self).contactus(**kwargs)
        values = dict(kwargs, error=[], kwargs=kwargs.items())
        return request.website.render(kwargs.get("view_from", "website.contactus"), values)

