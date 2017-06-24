# -*- coding: utf-8 -*-
#/#############################################################################
#
#    BizzAppDev
#    Copyright (C) 2004-TODAY bizzappdev(<http://www.bizzappdev.com>).
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
#/#############################################################################
{
    'name': 'Stop Phoning Home',
    'version': '10.0.1',
    'category': '',
    "sequence": 14,
    'complexity': "easy",
    'category': 'Extra Tools',
    'description': """
        Remove Few Phoning home feature effect from Core Odoo.

        The terms of the Odoo Enterprise Subscription Agreement do not allow disabling server requests to Odoo.com. For this reason, this module will not prevent communication with Odoo servers for Enterprise version.
    """,
    'author': 'BizzAppDev',
    'website': 'www.bizzappdev.com',
    'depends': ["mail",'web'],
    'init_xml': [],
    'data': [
        "base_view.xml",
        "mail_data.xml",
    ],
    'demo_xml': [],
    'test': [
    ],
    'qweb' : [
        "static/src/xml/base.xml",
    ],
    'installable': True,
    'auto_install': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
