# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################

from openerp import models, fields, api,_
from openerp.addons.decimal_precision import decimal_precision as dp

class OpenAccountChart(models.TransientModel):
    """
    For Chart of Accounts
    """
    _name = "account.open.chart"
    _description = "Account Open chart"
    
    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='posted')
    parent_needed = fields.Boolean('Parent Grouping Needed')

    def _build_contexts(self, data):
        result = {}
        result['state'] = data['target_move'] or ''
        result['date_from'] = data['date_from'] or False
        result['date_to'] = data['date_to'] or False
        result['strict_range'] = True if result['date_from'] else False
        return result

    @api.multi
    def account_chart_open_window(self):
        """
        Opens chart of Accounts
        @return: dictionary of Open account chart window on given date(s) and all Entries or posted entries
        """
        self.ensure_one()
        data = self.read([])[0]
        used_context = self._build_contexts(data)
        self  = self.with_context(used_context)
        if self.parent_needed:
            result = self.env.ref('account_parent.open_view_account_tree').read([])[0]
        else:
            result = self.env.ref('account_parent.open_view_account_noparent_tree').read([])[0]
        result_context = eval(result.get('context','{}')) or {}
        used_context.update(result_context)
        result['context'] = str(used_context)
        return result

    
class AccountAccount(models.Model):
    _inherit = 'account.account'
    
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
            balance = 0.0
            credit = 0.0
            debit = 0.0
            search_domain = default_domain[:]
            search_domain.insert(0,('account_id','=',account.id))
            for aml in self.env['account.move.line'].search(search_domain):
                balance += aml.debit - aml.credit
                credit += aml.credit
                debit += aml.debit
            account.balance = balance
            account.credit = credit
            account.debit = debit
    
    move_line_ids = fields.One2many('account.move.line','account_id','Journal Entry Lines')
    balance = fields.Float(compute="compute_values", digits_compute=dp.get_precision('Account'), string='Balance')
    credit = fields.Float(compute="compute_values",digits_compute=dp.get_precision('Account'), string='Credit')
    debit = fields.Float(compute="compute_values",digits_compute=dp.get_precision('Account'), string='Debit')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
