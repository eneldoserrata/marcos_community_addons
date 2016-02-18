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

from openerp.osv import fields, osv
import re
from openerp.report.render.rml2pdf import customfonts

class base_config_settings(osv.osv_memory):
    _inherit = 'base.config.settings'
        
    _columns = {
        'birthday_mail_template': fields.many2one('mail.template', 'Birthday Wishes Template', required=True,
            help='This will set the default mail template for birthday wishes.'),

    }


    def get_default_birthday_mail_template(self, cr, uid, fields, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return {'birthday_mail_template': user.company_id.birthday_mail_template.id}

    def set_birthday_mail_template(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context)
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        user.company_id.write({'birthday_mail_template': config.birthday_mail_template.id})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
