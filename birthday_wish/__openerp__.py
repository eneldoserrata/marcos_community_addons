# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 Medma - http://www.medma.net
#    All Rights Reserved.
#    Medma Infomatix (info@medma.net)
#
#    Coded by: Turkesh Patel (turkesh.patel@medma.in)
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
    "name": "Birthday Wish/Notifications",
    "version": "1.0",
    "author": "Medma Infomatix",
    "category": "Other",
    "website": "http://www.medma.net",
    "description": """In any business customer relations are most important and for any one their bithday is alwasy special so wish your clients using this module and improve your relations. Send Birthday Wishes via mail, get birthday Notifications and wish your customers.""",
    "summary": "Send Birthday Wishes via mail, get birthday Notifications and wish your customers",
    "license": "AGPL-3",
    "depends": ['base', 'mail'],
    'data':[
        'views/res_partner_view.xml',
        'views/res_config_view.xml',
        'data/template_data.xml',
        'data/wish_cronjob.xml',
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    "installable": True,
    "auto_install": False,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
