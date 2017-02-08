# -*- coding: utf-8 -*-

{
    'name': 'Save ReadOnly Fields',
    'summary': 'To allow save the readonly fields...',
    'description': """
Save ReadOnly Fields
====================

Save fields whit property 'readonly' activated...
""",

    'author': "Alejandro Cora González",
    'website': "",

    # Categories can be used to filter modules in modules listing.
    # Check /odoo/addons/base/module/module_data.xml for the full list.
    'category': '',
    'version': '1.0',

    # Any module necessary for this one to work correctly.
    'depends': [
        'web',
    ],

    # Always loaded.
    'data': [
        # Templates...
        'static/src/xml/webclient_templates.xml',
    ],

    # Only loaded in demonstration mode.
    'demo': [
    ],

    'test': [
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
