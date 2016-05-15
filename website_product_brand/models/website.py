# -*- coding: utf-8 -*-
##

from openerp.osv import orm
from openerp.http import request


class WebSite(orm.Model):
    _inherit = 'website'

    def sale_product_domain(self, cr, uid, ids, context=None):
        domain = super(WebSite, self).sale_product_domain(cr, uid, ids=ids,
                                                          context=context)
        if 'brand_id' in request.env.context:
            domain.append(
                ('product_brand_id', '=', request.env.context['brand_id']))
        return domain
