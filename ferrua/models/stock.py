# -*- coding: utf-8 -*-

from openerp import models, fields, api


class stock_move(models.Model):
    _inherit = "stock.pack.operation"

    position = fields.Integer(string=u'Posición')


    @api.model
    def create(self, vals):

        picking = self.env["stock.picking"].browse(vals.get("picking_id", False))

        order = False
        if picking.group_id.name:
            order = self.env["sale.order"].search([('name','=',picking.group_id.name)])

        product_id = vals.get("product_id", False)
        if order:
            for line in order.order_line:
                if line.product_id.id == product_id:
                    vals.update({"position":line.position})
                    break

        return super(stock_move, self).create(vals)
