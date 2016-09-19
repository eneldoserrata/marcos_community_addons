# -*- coding: utf-8 -*-
{
    'name': "Ferrua",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','stock','purchase','mrp','product_graphical_desing','mrp_sale_info','report'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/product.xml',
        'views/purchase.xml',
        'wizard/update_delivery_date_wizard_view.xml',
        'wizard/coil_pack_wizard.xml',
        'views/sale.xml',
        'views/bom_view.xml',
        'views/stock.xml',
        'views/account_invoice.xml',
        'reports/picking.xml',
        'reports/producer.xml',
        'reports/bom.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}