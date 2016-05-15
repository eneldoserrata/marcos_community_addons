{
    'name': 'Multi Images Product',
    'category': 'Website',
    'summary': 'Multi Images Product',
    'version': '1.0',
    'description': """
Multi Images Product
==================
        """,
    'website': 'www.templates-odoo.com',
    'author': 'DevTalents',
    'depends': [
       'product',
        'sale',
        'website_sale'
    ],
    'data': [
        'views/product_images.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}

