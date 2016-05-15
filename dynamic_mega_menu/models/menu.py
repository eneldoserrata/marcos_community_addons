# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class mega_menu(osv.osv):
    _inherit = "website.menu"

    _columns = {
        'mega_menu': fields.boolean('Mega Menu'),
    }


mega_menu()