# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.tools import float_compare

class account_payment(models.Model):
    _inherit = "account.payment"

    @api.one
    @api.depends('invoice_ids','move_line_ids.matched_debit_ids','move_line_ids.matched_credit_ids')
    def _compute_payment_balance(self):
        ids = []
        total_amount = 0.0
        for aml in self.move_line_ids:
            if aml.account_id.reconcile:
                ids.extend([r.debit_move_id for r in aml.matched_debit_ids] if aml.credit > 0 else [r.credit_move_id for r in aml.matched_credit_ids])
        for ml in ids:
            if self.payment_type == 'inbound':
                total_amount += ml.debit - ml.amount_residual
            else:
                total_amount += ml.credit - ml.amount_residual
        if total_amount > 0.0:
            set_amount = self.amount - total_amount
            if set_amount > 0.0:
                self.payment_balance = set_amount
            else:
                self.payment_balance = 0.0
        else:
            self.payment_balance = 0.0

        if not self.has_invoices:
            self.payment_balance = self.amount

    payment_balance = fields.Monetary(compute='_compute_payment_balance', string="Unapplied Balance",store="True", 
                                      help="What remains after deducting amounts already applied to close or reduce invoice balances.")

