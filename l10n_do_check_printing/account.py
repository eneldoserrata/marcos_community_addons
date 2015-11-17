# -*- coding: utf-8 -*-

from openerp import models, fields

class InheritedAccountJournal(models.Model):
    _inherit = "account.journal"

    do_check_layout = fields.Selection(string="Plantilla de cheque", required=True,
        help=u"Seleccione el formato que corresponde al papel de verificación va a imprimir sus cheques en.\n"
             u"Para desactivar la función de impresión, seleccione 'Ninguno'.",
        selection=[
            ('disabled', 'None'),
            ('l10n_do_check_printing.print_check_bpde', 'Banco Popular Empresarial'),
        ],
        default="disabled")

    do_check_multi_stub = fields.Boolean(u'Multi-Páginas talón de cheque',
        help=u"Esta opción le permite imprimir los detalles de verificación (stub) en varias páginas si no caben en una sola página.")

    do_check_margin_top = fields.Float('Margen superior', default=0.25,
        help=u"Ajuste los márgenes de cheques generados para que se ajuste la configuración de la impresora.")

    do_check_margin_left = fields.Float('Margen izquierdo', default=0,
        help=u"Ajuste los márgenes de cheques generados para que se ajuste la configuración de la impresora.")
