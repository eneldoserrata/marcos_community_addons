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


class stock_warehouse_inherit(osv.osv):
    _inherit = "stock.warehouse"
    _description = "Warehouse"
    
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Appartient à', required=True),
        'code': fields.char('Short Name', size=30,required=True, help="Short name used to identify your warehouse"),
    }



    @api.onchange('name')
    def _name_maj_warehouse(self):
        self.name = self.name.title() if self.name else False
         
    @api.onchange('code')
    def _code_maj_warehouse(self):
        self.code = self.code.title() if self.code else False
        