# -*- encoding: utf-8 -*-

from openerp import models, fields, api, exceptions, _


class HrExpenseExpense(models.Model):
    _inherit = 'hr.expense'

    def _prepare_move_line(self, line):
        res = super(HrExpenseExpense, self)._prepare_move_line(line)
        if self.invoice:
            if line['account_id'] == self.invoice.account_id.id:
                res['partner_id'] = \
                    self.invoice.partner_id.commercial_partner_id.id
        return res

    @api.multi
    def _move_line_get(self):
        account_move = []
        for expense in self:
            if expense.invoice:
                move_line = {
                    'type': 'src',
                    'name': expense.name.split('\n')[0][:64],
                    'price_unit': expense.unit_amount,
                    'quantity': expense.quantity,
                    'price': expense.total_amount,
                    'account_id': expense.invoice.account_id.id,
                    'product_id': False,
                    'uom_id': expense.product_uom_id.id,
                    'analytic_account_id': False,
                }
                account_move.append(move_line)
            else:
                if expense.product_id:
                    prod = expense.product_id.product_tmpl_id
                    account = prod._get_product_accounts()['expense']
                    if not account:
                        raise UserError(_("No Expense account found for the product %s (or for it's category), please configure one.") % (expense.product_id.name))
                else:
                    account = self.env['ir.property'].with_context(
                        force_company=expense.company_id.id).get(
                            'property_account_expense_categ_id',
                            'product.category')
                    if not account:
                        raise UserError(_('Please configure Default Expense account for Product expense: `property_account_expense_categ_id`.'))
                move_line = {
                        'type': 'src',
                        'name': expense.name.split('\n')[0][:64],
                        'price_unit': expense.unit_amount,
                        'quantity': expense.quantity,
                        'price': expense.total_amount,
                        'account_id': account.id,
                        'product_id': expense.product_id.id,
                        'uom_id': expense.product_uom_id.id,
                        'analytic_account_id': expense.analytic_account_id.id,
                    }
                account_move.append(move_line)

                # Calculate tax lines and adjust base line
                taxes = expense.tax_ids.compute_all(
                    expense.unit_amount,
                    expense.currency_id,
                    expense.quantity,
                    expense.product_id)
                account_move[-1]['price'] = taxes['total_excluded']
                account_move[-1]['tax_ids'] = expense.tax_ids.id
                for tax in taxes['taxes']:
                    account_move.append({
                        'type': 'tax',
                        'name': tax['name'],
                        'price_unit': tax['amount'],
                        'quantity': 1,
                        'price': tax['amount'],
                        'account_id': tax['account_id'] or move_line['account_id'],
                        'tax_line_id': tax['id'],
                    })
        return account_move

    @api.multi
    def action_move_create(self):
        """Reconcile supplier invoice payables with the created move lines."""
        res = super(HrExpenseExpense, self).action_move_create()
        for expense in self:
            if expense.invoice:
                partner = expense.invoice.partner_id.commercial_partner_id
                move_lines = expense.account_move_id.line_ids
                c_move_lines = move_lines.filtered(
                    lambda x: x.partner_id == partner and
                    x.debit == abs(round(expense.invoice.residual, 2)))
                c_move_lines |= expense.invoice.move_id.line_ids.filtered(
                    lambda x: x.account_id == expense.invoice.account_id and
                    x.credit == abs(round(expense.invoice.residual, 2)))
                if len(c_move_lines) != 2:
                    raise exceptions.Warning(
                        _('Cannot reconcile supplier invoice payable with '
                          'generated line. Please check amounts and see '
                          'if the invoice is already added or paid. '
                          'Invoice: %s') % expense.invoice.number)
                c_move_lines.reconcile()
        return res

    @api.multi
    def copy(self, default=None):
        res = super(HrExpenseExpense, self).copy(default)
        # Erase invoice references
        res.write({'invoice': False})
        return res

    invoice = fields.Many2one(
        comodel_name="account.invoice",
        string='Invoice',
        domain="[('type', '=', 'in_invoice'), ('state', '=', 'open')]")
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain=[('can_be_expensed', '=', True)],
        required=False)     # override from original True

    @api.one
    @api.onchange('invoice')
    def onchange_invoice(self):
        """Show in screen invoice data"""
        self.product_id = False
        self.date = self.invoice.date_invoice
        self.name = (self.invoice and self.invoice.reference) or ''
        self.analytic_account_id = False
        self.unit_amount = self.invoice.residual
        self.quantity = 1
        self.total_amount = self.unit_amount

    def _check_vals(self, vals):
        if vals.get('invoice'):
            # Rewrite values because readonly fields are not stored
            invoice = self.env['account.invoice'].browse(vals['invoice'])
            vals['product_id'] = False
            vals['date'] = invoice.date_invoice
            vals['analytic_account_id'] = False
            vals['unit_amount'] = invoice.residual
            vals['quantity'] = 1

    @api.model
    def create(self, vals):
        self._check_vals(vals)
        return super(HrExpenseExpense, self).create(vals)

    @api.multi
    def write(self, vals):
        self._check_vals(vals)
        return super(HrExpenseExpense, self).write(vals)
