{
    'name': 'Product Brand Manager',
    'category': 'Product',
    'summary': 'Product Brand Manager',
    'version': '1.0',
    'description': """
Product Brand Manager
==================
        """,
    'website': 'www.templates-odoo.com',
    'author': 'DevTalents',
    'depends': [
       'product',
        'sale',
    ],
    'data': [
        'views/product_brand_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}

