# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) BrowseInfo (http://browseinfo.in)
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
import datetime
from lxml import etree
import math
import pytz
import threading
import urlparse


from datetime import datetime, timedelta
from openerp import SUPERUSER_ID
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import UserError
from openerp.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT


class res_partner(models.Model):
    _inherit = "res.partner"


    birthdate = fields.Date(string='Date Of Birth', required=True, default=fields.Datetime.now)

    @api.model
    def _cron_birthday_reminder(self):
        su_id =self.env['res.partner'].browse(SUPERUSER_ID)
        for partner in self.search(()):
            bdate =datetime.strptime(partner.birthdate,'%Y-%m-%d').date()
            today =datetime.now().date()
            if bdate != today:
                if bdate.month == today.month:
                    if bdate.day == today.day:
                        if partner:
                            template_id = self.env['ir.model.data'].get_object_reference(
                                                                  'birthday_reminder',
                                                                  'email_template_edi_birthday_reminder')[1]
                            email_template_obj = self.env['mail.template'].browse(template_id)
                            if template_id:
                                values = email_template_obj.generate_email(partner.id, fields=None)
                                values['email_from'] = su_id.email
                                values['email_to'] = partner.email
                                values['res_id'] = False
                                mail_mail_obj = self.env['mail.mail']
                                msg_id = mail_mail_obj.create(values)
                                if msg_id:
                                    mail_mail_obj.send([msg_id])

        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
