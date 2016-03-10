# -*- coding: utf-8 -*-

# NOTE: this code write by Alexis de Lattre <alexis.delattre@akretion.com> on odoo module Currency Rate Date Check

from openerp import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.multi
    def _compute_multi_curr_enable(self):
        "check if multi company currency is enabled"
        company_currency = self.env['account.config.settings'].search([('group_multi_currency', '!=', False)])
        for company in self:
            company.multi_company_currency_enable = 1 if company_currency else 0

    @api.one
    def button_refresh_currency(self):
        """Refresh the currencies rates !!for all companies now"""
        self.services_to_use.refresh_currency()

    # Activate the currency update
    auto_currency_up = fields.Boolean(string=u'Actualización automática',
                                      help=u"La actualización automática de las monedas de esta empresa")
    # Function field that allows to know the
    # multi company currency implementation
    multi_company_currency_enable = fields.Boolean(string=u'Multi divisa de la empresa', translate=True,
                                                   compute="_compute_multi_curr_enable",
                                                   help=u"Cuando esta opción está desactivada se permite a los usuarios establecer unas actualizaciones de divisas distintas en cada empresa."
                                                   )
    # List of services to fetch rates
    services_to_use = fields.One2many('currency.rate.update.service', 'company_id',
                                      string=u'Servicios de actualización de divisas')

    currency_rate_max_delta = fields.Integer(string=u'Máximo de días permitidos en tasa', default=3,
                                             help=u"""Este es el máximo intervalo en días entre
                                                      la fecha asociada a la cantidad a convertir y la fecha
                                                      de la tasa de cambio más cercana disponible en Odoo.""")

    _sql_constraints = [
        ('currency_rate_max_delta_positive',
         'CHECK (currency_rate_max_delta >= 0)',
         u"El valor del campo 'Máximo de días permitidos en tasa' debe ser positivo o 0."),
    ]
