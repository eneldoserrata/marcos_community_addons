# -*- coding: utf-8 -*-
{
    'name': "General Enterprise theme",

    'summary': """
        Bring enterprise look and feel to Odoo community""",

    'description': """
        Bring enterprise look and feel to Odoo community
    """,

    'author': "Thành Loyal",
    'website': "http://www.nodo.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Theme',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}