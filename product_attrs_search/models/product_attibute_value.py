# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp.osv import osv, fields, expression


class product_attribute_value(osv.osv):
    _inherit = "product.attribute.value"
    _order = 'name'