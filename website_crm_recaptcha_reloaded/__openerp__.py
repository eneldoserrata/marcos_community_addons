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
{'name': 'Contact Form reCAPTCHA Reloaded',
 'version': '1.0',
 'category': 'Website',
 'depends': ['website_recaptcha_reloaded', 'website_crm','auth_signup'],
 'author': 'Tech Receptives',
 'license': 'AGPL-3',
 'website': 'https://www.techreceptives.com',
 'description': """
Odoo Contact Form reCAPTCHA Reloaded
=====================================
This modules allows you to integrate Google reCAPTCHA v2.0 to your website contact form.
You can configure your Google reCAPTCHA site and public keys
in "Settings" -> "Website Settings"
""",
 'data': [
     'views/website_crm.xml'
 ],
 'installable': False,
 'auto_install': False
}