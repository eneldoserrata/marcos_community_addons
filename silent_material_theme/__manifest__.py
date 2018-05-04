# -*- coding: utf-8 -*-
# Copyright 2016, 2017 Openworx
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Silent Material Theme",
    "summary": "Odoo 11 Silent Material Theme",
    "version": "11.0.1.0.2",
    "category": "Themes/Backend",
    "website": "https://www.silentinfotech.com",
	"description": """
		Silent Backend theme for Odoo 11.0 community edition.
    """,
	'images':[
        'images/screen.png'
	],
    "author": "Silentinfotech LLP",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'web_responsive',
        'backend_theme_v11'
    ],
    "data": [
        'views/assets.xml'
    ],
}

