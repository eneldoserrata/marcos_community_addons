# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################
from odoo import models, fields, api, _

class Product(models.Model):
    _inherit = 'product.template'

    length = fields.Char(
        string='Length',
    )
    width = fields.Char(
        string='Width',
    )
    height = fields.Char(
        string='Height',
    )
    dimensions_uom_id = fields.Many2one(
        'product.uom',
        'Dimension(UOM)',
        domain = lambda self:[('category_id','=',self.env.ref('product.uom_categ_length').id)],
        help="Default Unit of Measure used for dimension."
    )

    weight_uom_id = fields.Many2one(
        'product.uom',
        'Weight(UOM)',
        domain = lambda self:[('category_id','=',self.env.ref('product.product_uom_categ_kgm').id)],
        help="Default Unit of Measure used for weight."
    )
