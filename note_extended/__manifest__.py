# -*- coding: utf-8 -*-
{
    'name': 'Notes Extended',
    'version': '10.0.0.1',
    'description': """Adds extra functionality to Odoo Notes""",
    'summary': 'Auto archive notes',
    'author': 'Hugo Rodrigues',
    'website': 'https://hugorodrigues.net',
    'license': 'LGPL-3',
    'category': 'Tools',
    'depends': [
        'note',
    ],
    'data': [
        'views/note_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_instal': False
}
