{
    'name': 'POS Table Management',
    'version': '1.4',
    'category': 'Point of Sale',
    'author': 'TL Technology',
    'website': 'http://posodoo.com',
    'price': '0',
    "currency": 'EUR',
    'sequence': 0,
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'view/pos.xml',
        'template/pos_main.xml',
    ],
    'demo': ['data/tables.xml',],
    'test': [],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'installable': True,
    'license': 'LGPL-3',
    'support': 'thanhchatvn@gmail.com'
}
