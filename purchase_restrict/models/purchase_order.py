# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models,api,_
from openerp.exceptions import ValidationError

class purchase_order(models.Model):
    _inherit = 'purchase.order'
    
    @api.multi
    def button_confirm(self):
        zero_price = [x.product_id.name for x in self.order_line if not x.price_unit]
        if zero_price:
            if len(zero_price) > 1:
                message= _("This RFQ cannot be confirmed!\n\nThe following products have Unit Prices that haven't been set:") + '\n\n'
                message += '\n'.join(map(str,zero_price))
                message += '\n\nPlease edit the RFQ and make sure each item has a Unit Price.'
            else:
                message= _("This RFQ cannot be confirmed!\n\nThe following product has a Unit Price that hasn't been set:") + '\n\n'
                message += '\n'.join(map(str,zero_price))
                message += '\n\nPlease edit the RFQ and make sure this item has a Unit Price.'
            raise ValidationError(message.rstrip())
        else:
            return super(purchase_order,self).button_confirm()
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
