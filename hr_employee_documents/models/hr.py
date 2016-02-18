# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class hr_employee(osv.osv):
    _name = "hr.employee"
    _description = "Employee"
    _inherit = "hr.employee"

    def attachment_tree_view(self, cr, uid, ids, context):
        domain = ['&', ('res_model', '=', 'hr.employee'), ('res_id', 'in', ids)]
        res_id = ids and ids[0] or False
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, res_id)
        }

    def _get_attached_docs(self, cr, uid, ids, field_name, arg, context):
        res = {}
        attachment = self.pool.get('ir.attachment')
        for id in ids:
            employee_attachments = attachment.search(cr, uid, [('res_model', '=', 'hr.employee'), ('res_id', '=', id)], context=context, count=True)
            res[id] = employee_attachments or 0
        return res

    _columns = {
        'doc_count': fields.function(_get_attached_docs, string="Number of documents attached", type='integer')
    }
