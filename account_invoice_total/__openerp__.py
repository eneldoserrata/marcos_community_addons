# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Account Invoice Total",
    "version" : "1.9.1",
    "author" : "Bista Solutions",
    'category': 'Accounting & Finance',
    "summary": "Add total to Invoice list view (Bista)",
    'description': "For Odoo Enterprise Version 9.0, this module adds a total under the list view of Invoices, showing the Invoice and Refund net total.",
    'maintainer': "Bista Solutions",
    'website': 'http://www.bistasolutions.com/odoo-implementation-partners',
    "depends" : ["base","account_accountant"],
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [
        'views/account_invoice.xml',
    ],
    "test" : [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
