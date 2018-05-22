# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kanak Infosystems LLP. (<http://kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <http://kanakinfosystems.com/license>
#################################################################################

{
    'name': "OdooShoppe Backend Theme",
    'version': '1.0',
    'summary': 'Odooshoppe Backend Theme',
    'description': """
OdooShoppe - Backend Theme
================================
    """,
    'author': "Kanak Infosystems LLP.",
    'website': "http://www.kanakinfosystems.com",
    'images': ['static/description/main.gif'],
    'category': 'Theme/Backend',
    'depends': ['mail', 'calendar', 'base', 'base_geolocalize', 'website'],
    'images':['images/material5.png','images/material6.png','images/material7.png'],
    'data': [
        'views/material_app_switcher.xml',
        'views/material_osbt_templates.xml',
        'views/material_osbt_views.xml',
        'data/material_osbt_data.xml'
    ],
    'qweb': [
        'static/src/xml/material_osbt_templates.xml',
    ],
    'application': True,
    'license':'OPL-1',
    'price': 149,
    'currency': 'EUR',
    'live_test_url': 'http://v11.kanakinfosystems.com/web?db=backend_theme',
}
