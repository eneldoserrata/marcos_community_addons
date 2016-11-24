# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from openerp import models, fields, api, exceptions
import time
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow


class product_template_inherit(models.Model):
    _inherit = 'product.template'
     
    _sql_constraints = [ ('product_template_name_uniqu', 'unique(name)', 'Article existant !'),    ]
     
    @api.onchange('name')
    def _compute_maj_temp(self):
        self.name = self.name.title() if self.name else False
        
class product_pro_inherit(models.Model):
    _inherit = 'product.product'
     
    _sql_constraints = [ ('product_product_name_uniqu', 'unique(name)', 'Article existant !'),    ]    
 
    @api.onchange('name')
    def _compute_maj_pro(self):
        self.name = self.name.title() if self.name else False
        
