# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################
from openerp import api, fields, models, _

class AccountAccountType(models.Model):
    _inherit = "account.account.type"
    
    type = fields.Selection(selection_add=[('view','View')])
    

class AccountAccount(models.Model):
    _inherit = "account.account"
    
    parent_id = fields.Many2one('account.account','Parent Account')
    child_ids = fields.One2many('account.account','parent_id', 'Child Accounts')
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}
        if not context.get('show_parent_account',False):
            args += [('user_type_id.type', '!=', 'view')]
        return super(AccountAccount, self).search(args, offset, limit, order, count=count)
