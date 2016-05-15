# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today OpenERP SA (<http://www.openerp.com>).
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

import openerp
from openerp import tools

from openerp.osv import fields, osv
from openerp.tools.translate import _

import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request

import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_round


class res_partner(osv.osv):
    _inherit = "res.partner"
    
    _columns = {
        'partner_product_rel': fields.many2many('product.product', 'wishlist_partner_product_rel', 'user_id', 'product_id', 'Wishlist'),
    }
res_partner()



class product_wishlist(osv.osv):
    _name = "product.wishlist"
    
    _columns = {
                'name': fields.char('Name')
                }
    
product_wishlist()

class website(osv.osv):
    _inherit = 'website'
    
    def get_product_wishlist(self, cr, uid, context=None):
        ## GET ALL WISHLIST PRODUCT IN WISHLIST VIEW TO PERTICULAR USER(CURRENT LOGIN USER)
        new_product_ids = []
        reverse_product_ids =[]
        cr.execute("select product_id from wishlist_partner_product_rel where user_id = %s"%(uid))
        product_ids = [ i[0] for i in cr.fetchall()]
        for p_id in product_ids:
            product_id = self.pool.get('product.product').browse(cr,uid,p_id)
            if product_id:
                new_product_ids.append(product_id)
        for new_product_id in reversed(new_product_ids):
            reverse_product_ids.append(new_product_id)
        return reverse_product_ids
    
    def is_product_in_wishlist(self, cr, uid, product_id, context=None):
        ## CHECK IS PRODUCT ADDED TO WISHLIST AND HIDE WISHLIST MENU ON RETURN TRUE IN PRODUCT VIWE
        cr.execute("select product_id from wishlist_partner_product_rel where user_id = %s"%(uid))
        product_ids = [ i[0] for i in cr.fetchall()]
        for p_id in product_ids:
            if product_id == p_id:
                return True
        return False
    
    def check_product_is_in_cart(self, cr, uid, product_id, context=None):
        ## CHECK IS PRODUCT ADDED TO WISHLIST AND HIDE WISHLIST MENU ON RETURN TRUE IN PRODUCT VIWE
        order = request.website.sale_get_order(force_create=1)
        sale_order_obj = self.pool.get('sale.order.line')
        if order:
            sale_order_lines = sale_order_obj.search(cr, uid, [('order_id','=',order.id)])
            for sale_order_line in sale_order_lines:
                p_id = sale_order_obj.browse(cr, uid, sale_order_line).product_id.id
                if product_id == p_id:
                    return True
        return False
    
website()


class product_product(osv.osv):
    _inherit = "product.product"
    
    ## INHERIT CLASS FOR SETTING PRICE LIST TO WISHLIST TO SHOW DISCOUNT PRICE
    def _product_price(self, cr, uid, ids, name, arg, context=None):
        plobj = self.pool.get('product.pricelist')
        order = request.website.sale_get_order(force_create=1)
        price_list_id = order.pricelist_id
        if price_list_id:
            price_list_id = price_list_id.id
        res = {}
        if context is None:
            context = {}
        quantity = context.get('quantity') or 1.0
        pricelist = context.get('pricelist', False)
        partner = context.get('partner', price_list_id)
        pricelist = 1
        if pricelist:
            # Support context pricelists specified as display_name or ID for compatibility
            if isinstance(pricelist, basestring):
                pricelist_ids = plobj.name_search(
                    cr, uid, pricelist, operator='=', context=context, limit=1)
                pricelist = pricelist_ids[0][0] if pricelist_ids else pricelist

            if isinstance(pricelist, (int, long)):
                products = self.browse(cr, uid, ids, context=context)
                qtys = map(lambda x: (x, quantity, partner), products)
                pl = plobj.browse(cr, uid, pricelist, context=context)
                price = plobj._price_get_multi(cr,uid, pl, qtys, context=context)
                for id in ids:
                    res[id] = price.get(id, 0.0)
        for id in ids:
            res.setdefault(id, 0.0)
        return res
    
    _columns = {
               'price_inherit': fields.function(_product_price, type='float', string='Price', digits_compute=dp.get_precision('Product Price')),
                }
    
product_product()
