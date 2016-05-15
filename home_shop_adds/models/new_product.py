# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class new_product(osv.osv):
    _inherit = 'product.template'

    _columns = {
        'new_product': fields.boolean('Show it as new product at Homapage'),
    }


new_product()
