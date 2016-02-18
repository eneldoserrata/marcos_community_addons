# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 Medma - http://www.medma.net
#    All Rights Reserved.
#    Medma Infomatix (info@medma.net)
#
#    Coded by: Turkesh Patel (turkesh.patel@medma.in)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, orm, fields
from openerp.addons.base.ir.ir_qweb import HTMLSafe
from datetime import datetime, timedelta, time
from openerp.tools.translate import _

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'birth_date': fields.date('Birthdate'),
    }

    def send_birthday_email(self, cr, uid, ids=None, context=None):
        partner_obj = self.pool.get('res.partner')
        temp_obj = self.pool.get('mail.template')
        message_obj = self.pool.get('mail.message')
        channel_obj = self.pool.get('mail.channel')
        wish_template_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'birthday_wish', 'email_template_birthday_wish')[1]
        channel_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'birthday_wish', 'channel_birthday')[1]
        today = datetime.now()
        today_month_day = '%-' + today.strftime('%m') + '-' + today.strftime('%d')
        partner_ids = partner_obj.search(cr, uid, [('birth_date', 'like', today_month_day)])
        if partner_ids:
            for partner_id in partner_obj.browse(cr, uid, partner_ids, context=context):
                if partner_id.email:
                    temp_obj.send_mail(cr, uid, partner_id.company_id.birthday_mail_template and partner_id.company_id.birthday_mail_template.id or wish_template_id,
                                   partner_id.id, force_send=True, context=context)
                res = channel_obj.message_post(cr, uid, channel_id, body=_('Happy Birthday Dear %s.') % (partner_id.name), partner_ids=[partner_id.id], context=context)
                message_obj.write(cr, uid, res, {'channel_ids':[[6, False, [channel_id]]]}, context=context)
                self.message_post(cr, uid, [partner_id.id], body=_('Happy Birthday.'), context=context)
        return None
