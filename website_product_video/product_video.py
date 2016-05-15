# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class product_video(osv.Model):
    _inherit = 'product.template'

    _columns = {
        'name_video': fields.char('Name Video'),
        'description_video': fields.text('Description'),
        'iframe_video': fields.text('SRC iframe video'),

    }
product_video()

