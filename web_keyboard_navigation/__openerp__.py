# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (c) 2010-2012 Elico Corp. All Rights Reserved.
#
#    Author: Yannick Gouin <yannick.gouin@elico-corp.com>
#            Jerome Sonnet <jerome.sonnet@be-cloud.be> port to 9.0
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
    'name': 'Keyboard navigation',
    'version': '1.1',
    'category': 'Tools',
    'description': """
    This module add some keyboard shortcuts similar to the ones in the GTK-client.

    On a form, mode edit:
    Ctrl + S  :  Save the current object

    On a form, mode view:
    Ctrl + Delete      :  Delete the current object
    Ctrl + N           :  New object
    Ctrl + D           :  Duplicate the current object
    Ctrl + Z           :  Cancel the modification of current object
    Ctrl + Elico       :  Edit the current object
    Ctrl + Arrow Down  :  Next object
    Ctrl + Page Down   :  Last object
    """,
    "author": "be-cloud.be (Jerome Sonnet)",
    "website": "http://www.be-cloud.be",
    'depends': ['web'],
    'init_xml': [],
    'data': ['web_keyboard_navigation_view.xml'],
    'installable': True,
    'active': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: