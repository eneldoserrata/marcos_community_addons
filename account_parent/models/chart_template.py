# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################

from openerp import api, fields, models, _

class AccountAccountTemplate(models.Model):
    _inherit = "account.account.template"
    
    parent_id = fields.Many2one('account.account.template','Parent Account')
    
class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"
    
    @api.multi
    def generate_account(self, tax_template_ref, acc_template_ref, code_digits, company):
        account_tmpl_pool = self.env['account.account.template']
        account_pool = self.env['account.account']
        code_digits = 1
        account_template_account_dict = super(AccountChartTemplate, self).generate_account(tax_template_ref, acc_template_ref, code_digits, company)
        account_template_objs = account_tmpl_pool.browse(account_template_account_dict.keys())
        for account_template_obj in account_template_objs:
#             if account_template_obj.user_type_id and account_template_obj.user_type_id.type == 'view':
#                 account_obj = account_pool.browse(account_template_account_dict[account_template_obj.id])
#                 account_obj.write({'code': account_template_obj.code})
            if not account_template_obj.parent_id:
                continue
            account_parent_id = account_template_account_dict.get(account_template_obj.parent_id.id,False)
            account_obj = account_pool.browse(account_template_account_dict[account_template_obj.id])
            account_obj.write({'parent_id': account_parent_id})
        return account_template_account_dict