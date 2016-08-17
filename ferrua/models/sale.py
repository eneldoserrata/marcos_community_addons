# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
import re

import datetime


class Sale(models.Model):
    _inherit = "sale.order"

    delivery_date = fields.Date(u"Para entregar", copy=False)


    @api.onchange("delivery_date")
    def onchage_delivery_date(self):
        self.update_line_delivery_date()

    def update_line_delivery_date(self):
        for line in self.order_line:
            line.delivery_date = self.delivery_date


    @api.multi
    def action_confirm(self):
        for rec in self:
            mrp_exep = []
            for line in rec.order_line:
                route_ids = [route.id for route in line.product_id.route_ids]
                if 6 in route_ids:
                    product_bom = self.env["mrp.bom"].search([('product_id','=',line.product_id.id)])
                    if not product_bom:
                        mrp_exep.append(line.product_id.name_get()[0][1])

            if mrp_exep:
                res = ""
                for msg in mrp_exep:
                    res += u"{},\n".format(msg)
                raise exceptions.ValidationError(u"Es necesaria la lista de materiales para el producto:\n {}".format(res))

            if not rec.client_order_ref:
                raise exceptions.UserError(u"Para confirmar una orden coloque el número de la orden de compra del cliente en el campo: Referencia cliente para el pedido {}.".format(rec.name))

            client_order_ref = rec.search([('partner_id','=',rec.partner_id.id),
                                           ('client_order_ref','=',rec.client_order_ref),
                                           ('id', '!=', rec.id)])
            if client_order_ref:
                raise exceptions.ValidationError("La orden de compra en la referencia del cliente ya fue utilizada en el pedido {}".format(min(client_order_ref).name))
        return super(Sale, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    position = fields.Integer(u"Posición")
    delivery_date = fields.Date(u"Para entregar", copy=False)


    def _default_delivery_date(self):
        aDate = datetime.datetime.strptime(fields.Date.today(),"%Y-%m-%d")
        threeWeeks = datetime.timedelta(weeks=2)
        delivery_date =  aDate + threeWeeks
        return delivery_date.strftime("%Y-%m-%d")


    @api.onchange("position")
    def onchange_position(self):
        if self.position > 0:
            self.name = u"[POS: {}]: {}".format(self.position, self.name)
        else:
            self.name = self.name


    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        if not self.delivery_date:
            self.delivery_date = self._default_delivery_date()

        date_format = "%Y-%m-%d"
        start_date = datetime.datetime.strptime(fields.Date.today(), date_format)
        end_date = datetime.datetime.strptime(self.delivery_date, date_format)

        delta = end_date - start_date
        self.customer_lead = delta.days+2

        res = super(SaleOrderLine, self)._prepare_order_line_procurement(group_id)
        return res


class AccountInvoice(models.Model):
    _inherit = "account.invoice.line"

    stock_move_id = fields.One2many("stock.move", "invoice_line_id")


    @api.model
    def create(self, vals):
        temp = {'account_analytic_id': False,
                 'account_id': 3039,
                 'discount': 0.0,
                 'invoice_id': 159322,
                 'invoice_line_tax_ids': [(6, 0, [13])],
                 'name': u'[POS: 2]: [1023320] Salchicha Desayuno',
                 'origin': u'SO243',
                 'price_unit': 2974.82,
                 'product_id': 4883,
                 'quantity': 10.0,
                 'sale_line_ids': [(6, 0, [1080])],
                 'sequence': 11,
                 'uom_id': 22}
        res = super(AccountInvoice, self).create(vals)

        uom_obj = self.env['product.uom']
        for sale_line in res.sale_line_ids:
            qty_done = sum([uom_obj._compute_qty_obj(x.uom_id, x.quantity, x.product_id.uom_id) for x in sale_line.invoice_lines if x.invoice_id.state in ('open', 'paid')])
            quantity = uom_obj._compute_qty_obj(res.uom_id, res.quantity, res.product_id.uom_id)

            stock_moves = self.env['stock.move']

            for procurement in sale_line.procurement_ids:
                stock_moves |= procurement.move_ids
                stock_moves.sorted(lambda x: x.date)

            stock_moves = stock_moves.filtered(lambda r: r.state == "done" and not r.invoice_line_id)

            move_total_qty = sum([m.product_uom_qty for m in stock_moves])

            if move_total_qty == res.quantity:
                res.stock_move_id = stock_moves
            else:
                acumulado = 0
                for sm in stock_moves:
                    if sm.product_uom_qty == res.quantity:
                        res.stock_move_id = sm
                        break
        return res


class StockMove(models.Model):
    _inherit = "stock.move"

    invoice_line_id = fields.Many2one("account.invoice.line")



