# -*- coding: utf-8 -*-
###########################################################################
#    Copyright (c) 2015 Medma - http://www.medma.net
#    Copyright (C) 2016 - Today Turkesh Patel. <http://www.turkeshpatel.odoo.com>
#
#    Coded by: Turkesh Patel (turkesh.patel@medma.in)
#    @author Turkesh Patel (turkesh4friends@gmail.com)
#
##############################################################################


{
    "name": "Birthday Wish/Notifications",
    "version": "1.0",
    "author": "Turkesh Patel, Medma Infomatix",
    "category": "Other",
    "website": "http://turkeshpatel.odoo.com, http://www.medma.net",
    "description": """In any business customer relations are most important and for any one their bithday is alwasy special so wish your clients using this module and improve your relations. Send Birthday Wishes via mail, get birthday Notifications and wish your customers.""",
    "summary": "Send Birthday Wishes via mail, get birthday Notifications and wish your customers",
    "license": "AGPL-3",
    "depends": ['base', 'mail'],
    'data':[
        'views/res_partner_view.xml',
        'views/res_config_view.xml',
        'data/template_data.xml',
        'data/wish_cronjob.xml',
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    "installable": True,
    "auto_install": False,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
