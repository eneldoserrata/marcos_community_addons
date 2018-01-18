# -*- coding: utf-8 -*-
#############################################################################
#
#    BizzAppDev
#    Copyright (C) 2004-TODAY bizzappdev(<http://www.bizzappdev.com>).
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
#############################################################################

import logging
from odoo.tools.config import config
_logger = logging.getLogger(__name__)
from odoo.models import AbstractModel
from odoo import api
from odoo.release import version_info


class publisher_warranty_contract(AbstractModel):
    _inherit = "publisher_warranty.contract"

    @api.model
    def _get_message(self):
        if version_info and isinstance(version_info, (list,tuple)) and 'e' == version_info[-1]:
            ret =super(publisher_warranty_contract, self)._get_message()
            return ret
        return {}

    @api.model
    def _get_sys_logs(self):
        if version_info and isinstance(version_info, (list,tuple)) and 'e' == version_info[-1]:
            ret = super(publisher_warranty_contract, self)._get_sys_logs()
            return ret
        return

    @api.multi
    def update_notification(self, cron_mode=True):
        if version_info and isinstance(version_info, (list,tuple)) and 'e' == version_info[-1]:
            return super(publisher_warranty_contract, self).update_notification(cron_mode=cron_mode)
        _logger.info("NO More phoning Home Stuff")
        return True

    @api.model
    def set_notification_update(self, cron_id):
        if version_info and isinstance(version_info, (list,tuple)) and 'e' == version_info[-1]:
            self.env['ir.cron'].browse(cron_id).write({'active': True})
        else:
            self.env['ir.cron'].browse(cron_id).write({'active': False})
publisher_warranty_contract()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
