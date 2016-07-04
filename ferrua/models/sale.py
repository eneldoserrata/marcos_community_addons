# -*- coding: utf-8 -*-

from openerp import models, fields, api
import re

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    position = fields.Integer(u"Posición")

    @api.onchange("position")
    def onchange_position(self):
        if self.position > 0:
            self.name = u"[POS: {}]: {}".format(self.position, self.product_id.name)
        else:
            self.name = self.product_id.name

