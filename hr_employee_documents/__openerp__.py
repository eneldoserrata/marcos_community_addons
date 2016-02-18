# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Employee Documents',
    'version': '1.0',
    'category': 'Human Resources',
    'author': 'Osama Naoura',
    'description': """
By this module, you can attach one document or more to employee in HR module.
    """,
    'website': '',
    'depends': ['hr'],
    'data': [
        'views/hr_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
