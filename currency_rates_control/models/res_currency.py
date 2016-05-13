# -*- coding: utf-8 -*-

# NOTE: this code write by Alexis de Lattre <alexis.delattre@akretion.com> on odoo module Currency Rate Date Check


from openerp import models, fields, api



class res_currency_rate(models.Model):
    _inherit = "res.currency.rate"

    rate = fields.Float('Rate', digits=(12, 8), help='The rate of the currency to the currency of rate 1')
    name = fields.Date('Date', required=True, select=True)
