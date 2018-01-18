# -*- coding: utf-8 -*-
##############################################################################
#
#    iFenSys Software Solutions Pvt. Ltd.
#    Copyright (C) 2017 iFenSys Software Solutions(<http://www.ifensys.com>).
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Accounting Dashboard Bokeh Charts',
    'version': '10.0.0.1',
    'category':'Accounting',
    'summary': 'Accounting Dashboard Bokeh Charts',
    'author':'iFenSys Software Solutions Pvt. Ltd',
    'company':'iFenSys Software Solutions Pvt. Ltd',
    'website': 'http://www.ifensys.com',
    'depends': ['base','product','account'],
    'data': [
        'views/templates.xml',
        'data/dashboard_demo.xml',
        'data/dashboard_data.xml',
        'views/html_template_views.xml',
        'views/menus.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
