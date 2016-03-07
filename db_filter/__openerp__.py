# -*- coding: utf-8 -*-
{
    'name': "db_filter",

    'summary': """
        add proxy_set_header X_ODOO_DBFILTER <DBNAME> to nginx configuration
        to odoo return this db name
        """,

    'description': """

    """,

    'author': "Eneldo Serrata",
    'website': "http://marcos.do",

    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'auto_install': True
}