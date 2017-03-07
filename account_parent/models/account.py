# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp

class AccountAccountType(models.Model):
    _inherit = "account.account.type"
    
    type = fields.Selection(selection_add=[('view','View')])
    

class AccountAccount(models.Model):
    _inherit = "account.account"
    
    @api.model
    def _move_domain_get(self, domain=None):
        context = dict(self._context or {})
        domain = domain and safe_eval(str(domain)) or []
        
        date_field = 'date'
        if context.get('aged_balance'):
            date_field = 'date_maturity'
        if context.get('date_to'):
            domain += [(date_field, '<=', context['date_to'])]
        if context.get('date_from'):
            if not context.get('strict_range'):
                domain += ['|', (date_field, '>=', context['date_from']), ('account_id.user_type_id.include_initial_balance', '=', True)]
            elif context.get('initial_bal'):
                domain += [(date_field, '<', context['date_from'])]
            else:
                domain += [(date_field, '>=', context['date_from'])]

        if context.get('journal_ids'):
            domain += [('journal_id', 'in', context['journal_ids'])]

        state = context.get('state')
        if state and state.lower() != 'all':
            domain += [('move_id.state', '=', state)]

        if context.get('company_id'):
            domain += [('company_id', '=', context['company_id'])]

        if 'company_ids' in context:
            domain += [('company_id', 'in', context['company_ids'])]

        if context.get('reconcile_date'):
            domain += ['|', ('reconciled', '=', False), '|', ('matched_debit_ids.create_date', '>', context['reconcile_date']), ('matched_credit_ids.create_date', '>', context['reconcile_date'])]

        return domain
    
    
    @api.multi
    @api.depends('move_line_ids','move_line_ids.amount_currency','move_line_ids.debit','move_line_ids.credit')
    def compute_values(self):
        default_domain = self._move_domain_get()
        for account in self:
            sub_accounts = self.with_context({'show_parent_account':True}).search([('id','child_of',[account.id])])
            balance = 0.0
            credit = 0.0
            debit = 0.0
            search_domain = default_domain[:]
            search_domain.insert(0,('account_id','in',sub_accounts.ids))
            for aml in self.env['account.move.line'].search(search_domain):
                balance += aml.debit - aml.credit
                credit += aml.credit
                debit += aml.debit
            account.balance = balance
            account.credit = credit
            account.debit = debit
    
    move_line_ids = fields.One2many('account.move.line','account_id','Journal Entry Lines')
    balance = fields.Float(compute="compute_values", digits=dp.get_precision('Account'), string='Balance')
    credit = fields.Float(compute="compute_values",digits=dp.get_precision('Account'), string='Credit')
    debit = fields.Float(compute="compute_values",digits=dp.get_precision('Account'), string='Debit')
    parent_id = fields.Many2one('account.account','Parent Account',ondelete="set null")
    child_ids = fields.One2many('account.account','parent_id', 'Child Accounts')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)
    
    
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'code, name'
    _order = 'parent_left'
    
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}
        if not context.get('show_parent_account',False):
            args += [('user_type_id.type', '!=', 'view')]
        return super(AccountAccount, self).search(args, offset, limit, order, count=count)
    
class AccountJournal(models.Model):
    _inherit = "account.journal"
    
    @api.model
    def _prepare_liquidity_account(self, name, company, currency_id, type):
        res = super(AccountJournal, self)._prepare_liquidity_account(name, company, currency_id, type)
        # Seek the next available number for the account code
        code_digits = company.accounts_code_digits or 0
        if type == 'bank':
            account_code_prefix = company.bank_account_code_prefix or ''
        else:
            account_code_prefix = company.cash_account_code_prefix or company.bank_account_code_prefix or ''

        liquidity_type = self.env.ref('account_parent.data_account_type_view')
        parent_id = self.env['account.account'].search([('code','=',account_code_prefix),
                                                        ('company_id','=',company.id),('user_type_id','=',liquidity_type.id)], limit=1)
        
        if parent_id:
            res.update({'parent_id':parent_id.id})
        return res

