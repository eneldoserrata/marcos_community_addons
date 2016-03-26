# -*- encoding: UTF-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015-Today Key Concepts IT Services LLP.
#    (<http://keyconcepts.co.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': 'odoo9 POS Discount on Product',
    'version': '9.0',
    'author': 'Key Concepts IT Services LLP.',
    'website': 'http://keyconcepts.co.in',
    'category': 'Point-of-Sale',
    'description': """

=======================

Dispaly discount price with actual price in Point-of-Sale. 

""",
    'depends': ['point_of_sale'],
    'qweb': [
        'static/src/xml/pos_view.xml',
    ],
    'images': ['static/src/img/main_screenshot.png'],
}
