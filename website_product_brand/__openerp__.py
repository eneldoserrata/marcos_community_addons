{
    'name': 'Product Brand  Website',
    'category': 'e-commerce',
    'author': 'DevTalents',
    'website': 'www.templates-odoo.com',
    'version': '1.0',
    'depends': [
        'product_brand',
        'website_sale'
    ],
    'data': [
        "views/product_brand.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'auto_install': False,
}
