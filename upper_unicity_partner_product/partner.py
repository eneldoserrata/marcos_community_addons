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

     

class maj_uniq_partner(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [ ('res_fournisseur_name_uniqu', 'unique(name,supplier)', 'Ce nom existe déjà !'), ('res_client_name_uniqu', 'unique(name,customer)', 'Ce nom existe déjà !'), ]
#     _sql_constraints = [ ('res_client_name_uniqu', 'unique(name,customer)', 'Ce nom existe déjà !'),    ]
     
    @api.onchange('name')
    def _compute_maj_par(self):
        self.name = self.name.title() if self.name else False
        
