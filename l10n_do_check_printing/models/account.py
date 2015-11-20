# -*- coding: utf-8 -*-

from openerp import models, fields


class InheritedAccountJournal(models.Model):
    _inherit = "account.journal"

    check_layout = fields.Many2one("check.report.config", string="Plantilla de cheque", required=False,
        help=u"Seleccione el formato que corresponde al papel de verificación va a imprimir sus cheques en.\n"
             u"Para desactivar la función de impresión, seleccione 'Ninguno'.")

