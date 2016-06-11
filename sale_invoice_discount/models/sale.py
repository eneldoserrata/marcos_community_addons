# -*- coding: utf-8 -*-
##############################################################################
#
#    Sales and Invoice Discount Management
#    Copyright (C) 2015 BrowseInfo(<http://www.browseinfo.in>).
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

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import api, fields, models, _


class sale_order(models.Model):
    _inherit = 'sale.order'

    discount_method = fields.Selection([('fix', 'Fixed'), ('per', 'Percentage')], 'Discount Method')
    discount_amount = fields.Float('Discount Amount')
    discount_amt = fields.Monetary(compute='_amount_all', string='- Discount', digits_compute=dp.get_precision('Account'), store=True, readonly=True)

    @api.depends('discount_amount')
    @api.multi
    def _calculate_discount(self):
        res=0.0
        discount = 0.0
        for self_obj in self:
            if self_obj.discount_method == 'fix':
                discount = self_obj.discount_amount
                res = discount
            elif self_obj.discount_method == 'per':
                discount = self_obj.amount_untaxed * (self_obj.discount_amount/ 100)
                res = discount
            else:
                res = discount
        return res

    @api.depends('order_line.price_total','discount_amount')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        cur_obj = self.env['res.currency']
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                          'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                          'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                          'amount_total': amount_untaxed + amount_tax,
                          })
            res = self._calculate_discount()
            order.update({'discount_amt' : res,
                          'amount_total': amount_untaxed + amount_tax-res
                          })


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    is_apply_on_discount_amount =  fields.Boolean("Tax Apply After Discount")
    discount_method = fields.Selection([('fix', 'Fixed'), ('per', 'Percentage')], 'Discount Method')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:s
