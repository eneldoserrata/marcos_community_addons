# -*- coding: utf-8 -*-

from openerp import models, fields, api


class CheckReportConfig(models.Model):
    _name = "check.report.config"

    name = fields.Char("Nombre", required=True)

    body_top = fields.Float(string="Margen superior del cuerpo del cheque")

    name_top = fields.Float(string="Margen superior del nombre")
    name_left = fields.Float(string="Margen izquierdo del nombre")

    date_top = fields.Float(string="Margen superior de la fecha")
    date_left = fields.Float(string="Margen izquierdo de la fecha")

    amount_top = fields.Float(string="Margen superior del monto")
    amount_left = fields.Float(string="Margen izquierdo del monto")

    amount_letter_top = fields.Float(string="Margen superior monto en letras")
    amount_letter_left = fields.Float(string="Margen izquierdo monto en letras")

    check_header_top = fields.Float("Margen superior de la Cabecera")
    check_header = fields.Html("Cabecera del cheque")

    check_footer_top = fields.Float("Margen superior del pie")
    check_footer = fields.Html("Pie del cheque")