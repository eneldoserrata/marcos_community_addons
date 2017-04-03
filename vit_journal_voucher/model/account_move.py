from odoo import api, fields, models, _
import time
import logging
_logger = logging.getLogger(__name__)


class account_move(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    date = fields.Date(required=True,
                states={'posted': [('readonly', True)]}, index=True,
                string="Tanggal",
                default=fields.Date.context_today)
