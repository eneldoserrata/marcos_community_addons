
# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp import http
import json

PPG = 20 # Products Per Page
PPR = 3  # Products Per Row


class MyController(http.Controller):
    
    """ To Add Product To Wishlist Menu"""
    @http.route(['/shop/add_product_to_wishlist'], type='http', auth="public", website=True)
    def add_product_to_wishlist(self, product_id=False):
        cr, uid, context = request.cr, request.uid, request.context
        cr.execute('insert into wishlist_partner_product_rel(product_id,user_id)values(%s,%s)', (product_id, uid))
        return request.redirect("#")
    
    
    @http.route(['/shop/add_product_to_wishlist_from_cart/product_id'], type='http', auth="public", website=True)
    def add_product_to_wishlist_from_cart(self, product_id=False):
        cr, uid, context = request.cr, request.uid, request.context
        cr.execute('insert into wishlist_partner_product_rel (product_id,user_id) values (%s,%s)', (product_id, uid))
        return request.redirect("#")
    
    @http.route(['/shop/add_product_to_wishlist_from_shop/product_id'], type='http', auth="public", website=True)
    def add_product_to_wishlist_from_shop(self, product_id=False):
        cr, uid, context = request.cr, request.uid, request.context
        cr.execute('insert into wishlist_partner_product_rel (product_id,user_id) values (%s,%s)', (product_id, uid))
        return request.redirect("#")
    
    
    """ To Remove Product From Wishlist Menu"""
    @http.route(['/shop/remove_product_from_wishlist/product_id'], type='http', auth="public", website=True)
    def remove_product_from_wishlist(self, product_id=False):
        cr, uid, context = request.cr, request.uid, request.context
        if product_id:
            cr.execute('delete from wishlist_partner_product_rel where product_id = %s and user_id = %s' %(product_id, uid))
        data ={}
        data["message"] = "Added Successfully"
        return  json.dumps(data)
    
    """ To Remove Product From Wishlist Menu"""
    @http.route(['/shop/remove_product_from_wishlist_form/'], type='http', auth="public", website=True)
    def remove_product_from_wishlist1(self, product_id=False):
        cr, uid, context = request.cr, request.uid, request.context
        if product_id:
            cr.execute('delete from wishlist_partner_product_rel where product_id = %s and user_id = %s' %(product_id, uid))
        return request.redirect("#")
    
    """ To View wishlist menu to view all product"""
    @http.route(['/shop/view_my_wishlist'], type='http', auth="public", website=True)
    def view_my_wishlist(self, product_id=False):
        cr, uid, context = request.cr, request.uid, request.context
        cr.execute("select product_id from wishlist_partner_product_rel")
        product_ids = cr.fetchall()
        values ={
                 'product_id': product_id,
                 'uid': uid,
                 }
        return request.website.render("wishlist.suggested_wish_list_id",values)
    
    
    """    TO ADD PRODUCT TO MY CART FROM WISHLIST """
    @http.route(['/shop/move_product_to_cart/product_id'], type='http', auth="public", website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        # HANDLING INVALID "add_qty" VALUES
        data ={}
        try:
            add_qty = float(add_qty)
        except ValueError:
            #this.do_warn(_t("The following fields are invalid:"), warnings.join(''));
            return None
        if add_qty <= 0.0:
            return None
        cr, uid, context = request.cr, request.uid, request.context
        sale_order_line = request.website.sale_get_order(force_create=1)._cart_update(product_id=int(product_id), add_qty=add_qty, set_qty=float(set_qty))
        data["message"] = "Added Successfully"
        if sale_order_line:
            cr.execute('delete from wishlist_partner_product_rel where product_id = %s and user_id = %s' %(product_id, uid))
        return  json.dumps(data)
    
    
    @http.route(['/shop/check_for_variant/product_id'], type='http', auth="public", website=True)
    def check_for_variant(self, product_id=False):
        cr, uid, context = request.cr, request.uid, request.context
        data ={}
        cr.execute("select 1 from wishlist_partner_product_rel where user_id = %s and product_id = %s"%(uid,product_id))
        result = [ i[0] for i in cr.fetchall()]
        data["message"] = False
        data["product_id"] = product_id
        if result:
            data["message"] = True
            data["product_id"] = product_id
        return  json.dumps(data)
    
    
    
    @http.route(['/shop/check_product_is_in_cart/product_id'], type='http', auth="public", website=True)
    def check_product_is_in_cart(self, product_id=False):
        cr, uid, context = request.cr, request.uid, request.context
        data ={}
        order = request.website.sale_get_order(force_create=1)
        data["message"] = "Added Successfully"
        return  json.dumps(data)
