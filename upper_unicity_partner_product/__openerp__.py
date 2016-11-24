# -*- coding: utf-8 -*-


{
    'name': 'Upper case Customers/Suppliers/Products/Entrepôts & Unicity',
    'version': '1.1',
    'category': 'Upper case',
    'sequence': 200,
    'summary': 'Transformation min/maj, unicité',
    'description': """
    Module complémentaire    """,
    'author': 'Othmane GHANDI, Badr EL MAROUANI',
    "website" : "http://www.osisoft.ma",
    'depends': ['base','sale','purchase','stock'],
    'images': ['images/main_screenshot.png'],
    'data': [
             'views/warehouse_view_inherited.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
