# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    old_id = fields.Integer()


class ResPartner(models.Model):
    _inherit = "product.template"

    old_id = fields.Integer()


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    parent_id = fields.Integer()
    state_old = fields.Char()
