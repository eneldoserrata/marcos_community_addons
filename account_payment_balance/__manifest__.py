# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'license': 'LGPL-3',
    "name" : "Account Payment Balance",
    "version" : "1.10.1",
    "author" : "Bista Solutions",
    'category': 'Accounting',
    "summary": "Add Unapplied Balance to Payments (Bista)",
    'description': "For Odoo Version 10.0, this module shows the unapplied balance of Payments on the list and form view, with a filter to show payments with a positive unapplied balance.",
    'maintainer': "Bista Solutions",
    'website': 'http://www.bistasolutions.com/erp-implementation-company/erp-customization-company',
    "depends" : ["base","account_accountant"],
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [
        'views/account_payment.xml',
    ],
    "test" : [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
