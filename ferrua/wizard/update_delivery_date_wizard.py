# -*- coding: utf-8 -*-

from openerp import models, fields, api


class UpdateDeliveryDateWizard(models.TransientModel):
    _name = "update.delivery.date.wizard"

    delivery_date = fields.Date("Fecha de entrega para todos los productos de la orden", required=True)

    @api.multi
    def update_line_delivery_date(self):
        active_id = self._context.get("active_id", False)
        if active_id:
            order = self.env["sale.order"].browse(active_id)
            order.delivery_date = self.delivery_date
            for line in order.order_line:
                line.delivery_date = self.delivery_date