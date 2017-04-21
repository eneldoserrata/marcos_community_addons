# -*- encoding: utf-8 -*-
from openerp import api, fields, models, _
from datetime import datetime, timedelta, time

class res_partner(models.Model):
    _inherit = 'res.partner'

    birth_date = fields.Date('Birthdate')

    @api.multi
    def send_birthday_email(self):
        ir_data = self.env['ir.model.data']
        wish_template = ir_data.get_object('birthday_wish', 'email_template_birthday_wish')
        channel = ir_data.get_object('birthday_wish', 'channel_birthday')
        today = datetime.now()
        today_month_day = '%-' + today.strftime('%m') + '-' + today.strftime('%d')
        for partner in self.search([('birth_date', 'like', today_month_day)]):
            if partner.email:
                if partner.company_id.birthday_mail_template and partner.company_id.birthday_mail_template.id:
                    partner.company_id.birthday_mail_template.sudo().send_mail(partner.id, force_send=True)
                else:
                    wish_template.sudo().send_mail(partner.id, force_send=True)
            res = channel.message_post(body=_('Happy Birthday Dear %s.') % (partner.name), partner_ids=[partner.id])
            res.write({'channel_ids':[[6, False, [channel.id]]]})
            partner.message_post(body=_('Happy Birthday.'))
        return None