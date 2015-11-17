# -*- coding: utf-8 -*-

from openerp import models, fields


class InheritedBank(models.Model):
    _inherit = "res.bank"

    statement_import_type = fields.Selection([('bpdofx','OFX')], string=u"Formato de importación de extractos")