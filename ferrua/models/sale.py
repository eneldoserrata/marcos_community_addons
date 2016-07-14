# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
import re


class Sale(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        for rec in self:
            mrp_exep = []
            for product in rec.order_line:
                routes_to_built = [route.id for route in product.product_tmpl_id.route_ids if route.id == 6]
                if routes_to_built and not product.product_tmpl_id.bom_count:
                    mrp_exep.append(product.product_tmpl_id.name)

            if mrp_exep:
                res = ""
                for msg in mrp_exep:
                    res += u"{},\n".format(msg)
                raise exceptions.ValidationError(u"Es necesaria la lista de materiales para el producto:\n {}".format(res))

        return super(Sale, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    position = fields.Integer(u"Posición")

    @api.onchange("position")
    def onchange_position(self):
        if self.position > 0:
            self.name = u"[POS: {}]: {}".format(self.position, self.product_id.name)
        else:
            self.name = self.product_id.name