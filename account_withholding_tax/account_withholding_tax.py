# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) {2014} {Burgundy} <{admin@burgundylabs.com}>
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp import api, fields, models
from openerp.exceptions import UserError


class account_withholding_tax(models.Model):
    
    _name = "account.withholding.tax"
    _description = "Withholding Tax"

    name = fields.Char(string='Name', required=True)
    percentage = fields.Float(string='Percentage')
    type = fields.Selection([('sale', 'Sales'), ('purchase', 'Purchases')], string='Tax Application', default='purchase', required=True)
    account_id = fields.Many2one('account.account', string='Tax Account', required=True)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Unfortunately this name is already used, please choose a unique one'),
    ]
            
    @api.one
    @api.constrains('percentage')
    def _check_percentage(self):
        if self.percentage > 100 or self.percentage < 0:
            raise UserError(_('Error!'), _('The Percentage are invalid.\nNegative numbers and percentage\nover 100 are not allowed.'))

class account_invoice(models.Model):
    
    _inherit = 'account.invoice'
    
    @api.one
    @api.depends('invoice_line_ids.amount_wht_line', 'amount_total', 'tax_line_ids.amount', 'currency_id', 'company_id')
    def _compute_amount_wht(self):
        self.net_pay = self.amount_total - self.amount_wht
        self.amount_wht = sum(line.amount_wht_line for line in self.invoice_line_ids if line.amount_wht_line)
        
    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        self.ensure_one()
        wht_lines = {}
        for line in self.invoice_line_ids:
            if line.wht_id:
                wht_lines[line.wht_id] = wht_lines.get(line.wht_id, 0.0) + line.amount_wht_line
        for wht_id in wht_lines.keys():    
            move_lines.append((0, 0, {
                                    'name': wht_id.name,
                                    'credit': wht_lines[wht_id],
                                    'debit': False,
                                    'partner_id': self.partner_id.id,
                                    'account_id': wht_id.account_id.id
                                    }))
        for line in move_lines:
            if line[2].get('invoice_id') and line[2].get('account_id') == self.account_id.id :
                line[2]['credit'] -= sum(wht_lines.values())
                
        return super(account_invoice, self).finalize_invoice_move_lines(move_lines)
    
    amount_wht = fields.Monetary(string='Withholding Amount',
        store=True, readonly=True, compute='_compute_amount_wht', track_visibility='onchange')
    net_pay = fields.Monetary(string='Net Pay',
        store=True, readonly=True, compute='_compute_amount_wht', track_visibility='onchange')
    
class account_invoice_line(models.Model):
    
    _inherit = 'account.invoice.line'

    @api.one
    @api.depends('price_subtotal', 'wht_id')
    def _compute_price_wht(self):
        percentage = self.wht_id.percentage or 0.0
        self.amount_wht_line = self.price_subtotal * (percentage / 100.0)

    wht_id = fields.Many2one('account.withholding.tax', string='WH Taxes')
    amount_wht_line = fields.Monetary(string='Wht Amount',
        store=True, readonly=True, compute='_compute_price_wht')
