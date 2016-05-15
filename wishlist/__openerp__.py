{
    'name': 'Product Wishlist',
    'category': 'Website',
    'summary': 'Add Products To Wishlist',
    'website': 'www.dev-talents.com',
    'version': '1.0',
    'description': """
Product Wishlist
==================

        """,
    'author': 'DevTalents',
    'depends': ['website_sale'],
    'data': [
        'views/template.xml',
        'views/wishlist_template_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],

    'installable': True,
    'application': True,
}
