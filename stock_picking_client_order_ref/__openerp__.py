# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Roberto Barreiro (<roberto@disgal.es>)
#    All Rights Reserved
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Stock Picking Client Order Reference',
    'version': '9.0.1.1',
    'category': 'Sales Management',
    'sequence': 10,
    'summary': 'Client order reference on delivery orders',
    'description': """
This module adds a field on delivery orders with the client order reference given on quotations or sale orders.
    """,
    'author': 'Roberto Barreiro',
    'depends': ['sale','stock',],
    'data': ['views/stock_picking_client_order_ref_view.xml', 'views/report_picking_client_order_ref_view.xml',],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
