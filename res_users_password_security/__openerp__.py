# -*- coding: utf-8 -*-
# © 2015-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{

    'name': 'Password Security',
    "summary": "Allow admin to set password security requirements.",
    'version': '9.0.1.0.0',
    'author': "LasLabs",
    'category': 'Base',
    'depends': [
        'auth_signup',
    ],
    "website": "https://laslabs.com",
    "licence": "AGPL-3",
    "data": [
        'views/res_company_view.xml',
    ],
    'test': [
        'tests/company.yml',
    ],
    'installable': True,
    'auto_install': False,
}
