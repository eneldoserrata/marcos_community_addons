# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2015 OpenERP4you (<http://openerp4you.in>).
#    All Rights Reserved
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
    "name": "Dynamic Report Export",
    "version": "1.0",
    "depends": [],
    "author": "Pradeep Singh (OpenERP4You)",
    "category": "Custom",
    "description": """
    This Module can be used to export the XLS reports of the choosen objects using different parameters
    
    """,
    "init_xml": [],
    "data" :['dynamic_report_wiz.xml'],
    'update_xml': [ ],
    'demo_xml': [],
    'js':[],
    'qweb':[],
    'css':[],
    'img':['static/src/img/*'],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}
