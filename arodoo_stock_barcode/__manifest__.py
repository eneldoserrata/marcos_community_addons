# -*- coding: utf-8 -*-
{
    'name': "Warehouse Barcode",

    'summary': """
        Barcode module works like Odoo 10 enterprise version.
        """,

    'description': """
        This module helps you use the barcode scanner to receive or deliver shipment.
        This module works on Picking page without any pre-configuration, Just install the module and enjoy it.
        Provided by: arodoo.com
    """,

    'author': "ARODOO.COM",
    'website': "http://www.arodoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'barcodes'],

    # always loaded
    'data': [
        'views/templates.xml',
        'views/stock_picking_view.xml',
        'views/stock_pack_operation_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}