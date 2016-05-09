
# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'license': 'LGPL-3',
    "name" : "Request for Quotation Price Validation",
    "version" : "1.9.1",
    "author" : "Bista Solutions, Serpent Consulting Services",
    'category': 'Purchases',
    "summary": "RFQ/Draft PO products must have non Zero Unit Price (Bista)",
    'description': 
""" 
For Odoo Enterprise Version 9.0, this module ensures that all items on a Draft PO/Request for Quotation have a Unit Price set.
""",
    'maintainer': "Bista Solutions",
    'website': 'http://www.bistasolutions.com/odoo-implementation-partners',
    "depends" : ["base","purchase"],
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [],
    "test" : [],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
