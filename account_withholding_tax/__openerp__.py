# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) {2014} {Burgundy} <{admin@burgundylabs.com}>
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

{
    'name': 'Withholding Taxes (Pajak Penghasilan)',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'summary': 'Withholding Taxes (Pajak Penghasilan) in Invoices',
    'description': """
Withholding Taxes (Pajak Penghasilan) in Invoice 
""",
    'author': 'Burgundy Teknologi',
    'website': 'www.burgundylabs.com',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'account_withholding_tax_view.xml',
        "security/ir.model.access.csv",
    ],
    "images": [
        "images/aturan-pajak.jpg"
    ],
}
