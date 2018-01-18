# -*- coding: utf-8 -*-
# © 2017 Tobias Zehntner
# © 2017 Niboo SPRL (https://www.niboo.be/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):
        """
        If mail has exception, leave note on record's chatter box
        """
        super(MailMail, self).send(auto_commit, raise_exception)
        for mail in self.filtered(lambda m: m.state == 'exception'):
            record = self.env[mail.model].browse(mail.res_id)
            reason = mail.failure_reason
            mail.note_delivery_failure(record, reason)

        return True

    @api.multi
    def note_delivery_failure(self, record, reason):
        """
        Note mail delivery failure on chatter box
        """
        message = 'Mail Delivery Failure: %s' % reason
        context = {'no_failure_note': True}

        if record.user_id:
            record.message_subscribe([record.user_id.partner_id.id])
        if not self._context.get('no_failure_note', False):
            record.with_context(context).message_post(
                message, subtype='mail.mt_note',
                message_type='notification')
