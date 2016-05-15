{
    'name': 'Dynamic Mega Menu',
    'category': 'Website',
    'summary': 'Dynamic Mega Menu',
    'version': '1.0',
    'website': 'www.templates-odoo.com',
    'author': 'DevTalents',
    'depends': [
       'website',
    ],
    'data': [
        'backend_views/mega_menu.xml',
        'data/menu.xml',
        'views/submenu_generation.xml',
    ],
    'installable': True,
    'application': True,
}
