# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
import re

import datetime


class Sale(models.Model):
    _inherit = "sale.order"

    delivery_date = fields.Date(u"Para entregar", copy=False)

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
            positions = re.findall(u"\[POS\: ?[0-9]+\]\:", self.name)
            for pos in positions:
                self.name = self.name.replace(pos, "")
            self.name = u"[POS: {}]: {}".format(self.position, self.name.strip())
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


    def update_lst_price(self, date, price, product_id):
        company_currency = self.company_id.currency_id
        price_list_currency = self.order_id.pricelist_id.currency_id
        if company_currency.id != price_list_currency.id:
            new_price = price_list_currency.with_context({'date': date}).compute(price, company_currency,round=False)
        else:
            new_price = self.price_unit

        self.env["product.product"].browse(product_id).write({'lst_price': new_price})


    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        if vals.get("price_unit", False):
            self.update_lst_price(res.create_date, res.price_unit, res.product_id.id)
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        for rec in self:
            if vals.get("price_unit", False):
                self.update_lst_price(rec.create_date, rec.price_unit, rec.product_id.id)
        return res



    # @api.onchange('price_unit')
    # def product_uom_change(self):
    #     if self.product_id:
    #         self.update_lst_price(self.create_date, self.price_unit, self.product_id.id)

        # company_currency = self.company_id.currency_id
        # price_list_currency = self.order_id.pricelist_id.currency_id
        #
        # if company_currency.id != price_list_currency.id:
        #     new_price = price_list_currency.with_context({'date': self.create_date}).compute(self.price_unit, company_currency,round=False)
        # else:
        #     new_price = self.price_unit
        #
        # if new_price and self.product_id:
        #     self.env["product.product"].browse(self.product_id.id).write({'lst_price': new_price})








