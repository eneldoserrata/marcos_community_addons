# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Rui Pedrosa Franco All Rights Reserved
#    http://pt.linkedin.com/in/ruipedrosafranco
#    $Id$
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
    'name'          : 'Developer tweaks',
	'version'       : '1.0',
	'category'      : 'Extra tools',
    'summary'       : 'Tweaks to help developers',
	'description'   : """
- creates a 'Odoo Developer' group
- admin user becomes part of the developer group
- users belonging to developer group...
    . belong to the Administration/Settings group
    . have "Technical Features" set
    . see new menu to see recently updated modules
    . see new top menu link to reupdate latest updated module
    . see database's name on top of the company's logo
    . see update button in module's kanban view
    . see latest update in all module views
- better logging
                        """,
	'author'        : 'Rui Pedrosa Franco',
	'website'       : 'http://pt.linkedin.com/in/ruipedrosafranco',
	'depends'       : ['base'],
	'data'          : [
                       'security/security_data.xml',
                       'developer_tweaks_view.xml',
                        ],
    'installable'   : True,
    'active'        : False,
    'auto_install'  : True
}
