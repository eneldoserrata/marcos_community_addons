# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _, tools

_logger = logging.getLogger(__name__)


class mail_compose_message(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.multi
    def send_mail(self, auto_commit=False):
        return super(mail_compose_message, self.with_context(from_composer=True)).send_mail(auto_commit=auto_commit)
