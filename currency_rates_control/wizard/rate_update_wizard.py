# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

import logging

_logger = logging.getLogger(__name__)


class RateUpdateWizard(models.TransientModel):
    _name = "update.rate.wizard"

    update_method = fields.Selection([('server','Desde internet'),('manual','Introducir tasa manualmente')],
                                   string=u"Metodo de actualizaciónn de tasa", default="server")
    name = fields.Date("Fecha", required=True)
    rate = fields.Float("Monto", requiered=True)
    currency_id = fields.Many2one("res.currency", string="Moneda", readonly=True)

    @api.multi
    def update_rate(self):
        if self.update_method == "manual":
            if self.rate < 1:
                raise exceptions.UserError("El valor de la tasa debe de ser mayor que 0")
            rate = self.env["res.currency.rate"].search([('name','=',self.name),('currency_id','=',self.currency_id.id)])
            if rate:
                return rate.write({"rate": 1/self.rate})
            else:
                return self.env["res.currency.rate"].create({"name": self.name, "rate": 1/self.rate, "currency_id": self.currency_id.id})
        else:
            try:
                self.env["currency.rate.update.service"]._run_currency_update()
            except Exception as e:
                _logger.error("{}".format(e))
                raise exceptions.ValidationError("Ocurrio un error al intentar actualizar la tasa desde el servidor de internet.")



