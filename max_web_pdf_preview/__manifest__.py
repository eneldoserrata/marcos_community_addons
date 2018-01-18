# -*- coding: utf-8 -*-
##############################################################################
#    Web PDF Report Preview & Print
#    Copyright 2014 wangbuke <wangbuke@gmail.com>
#    
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

{
    "name": "Web PDF Report Preview & Print",
    'version': '10.0.0.1',
    'category': 'Web',

    'summary': """
        To Preview & Print PDF report in your browser.
    """,

    'description': """Web PDF Report Preview & Print

Preview & Print PDF report in your browser.

* For IE, Adobe Reader is required.
* For Chrome , nothing is requried.
* For Firefox, Adobe Reader is required.


If your brower prevented pop-up window, you should allow it.

    """,

    'author': 'wangbuke@gmail.com, MAXodoo',
    'website': 'http://buke.github.io',
    'license': 'AGPL-3',
    'depends': ['web'],
    'data': [
        'views/max_web_pdf_preview_view.xml',
    ],
}

