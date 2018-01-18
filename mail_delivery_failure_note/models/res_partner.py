# -*- coding: utf-8 -*-
# © 2017 Tobias Zehntner
# © 2017 Niboo SPRL (https://www.niboo.be/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _notify(self, message, force_send=False, send_after_commit=True,
                user_signature=True):
        """
        Check if any subscribers have turned off email notifications and
        leave delivery failure note on record
        """
        message_sudo = message.sudo()
        email_channels = message.channel_ids.filtered(
            lambda channel: channel.email_send)
        partner_ids = self.sudo().search([
            '|',
            ('id', 'in', self.ids),
            ('channel_ids', 'in', email_channels.ids),
            ('email', '!=', message_sudo.author_id
                            and message_sudo.author_id.email
                            or message.email_from)])
        no_notify_partner_ids = partner_ids.filtered(
            lambda p: p.notify_email == 'none')

        if no_notify_partner_ids:
            record = message.env[message.model].browse(message.res_id)
            reason = 'The following subscribers have email notifications ' \
                     'turned off: %s' % ', '.join([p.name
                                                   for p in partner_ids])
            self.env['mail.mail'].note_delivery_failure(record, reason)

        super(ResPartner, self)._notify(message, force_send, send_after_commit,
                                        user_signature)
        return True
