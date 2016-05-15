{
    'name': 'Home shop adds',
    'category': 'Website',
    'summary': 'Home shop adds',
    'version': '1.0',
    'description': """
Home shop adds
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
        'views/new_product.xml',
    ],
    'installable': True,
    'application': True,
}
