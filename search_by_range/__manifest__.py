# -*- coding: utf-8 -*-
{
    'name': 'Search By Range',
    'version': '1.0',
    'category': 'web',
    'summary': 'Search by date range in List view and Pivot view',
    'description': """

Search by date range in List view and Pivot view
--------------------------------------------------

    """,
    'author': 'SkyERP',
    'website': 'https://skyerp.net',
    'depends': ['web'],
    'data': [
        'views/template_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    "price": 0.00,
    "currency": "EUR",
    
    'images': ['static/description/list_pivot.png'],

    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
