# -*- encoding: utf-8 -*-
##############################################################################
#    L.S.C.A. German Ponce Dominguez
#    german.ponce@outlook.com
##############################################################################

from openerp import api, fields, models, _, tools, release
from datetime import datetime
import time
from openerp import SUPERUSER_ID
import time
import dateutil
import dateutil.parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from openerp.exceptions import UserError, RedirectWarning, ValidationError
from openerp.tools import float_compare, float_round

from datetime import date, datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


from datetime import datetime,time, timedelta


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    period_fiscal  = fields.Char(compute='_get_period_from_date', string='Periodo Fiscal', store=True
                                )
    
    year_fiscal  = fields.Char(compute='_get_fiscalyear_from_date', string='Año Fiscal', store=True
                                )
    
    @api.one
    @api.depends('date_invoice')
    def _get_period_from_date(self):
        if self.date_invoice:
            date_invoice = self.date_invoice
            year_fiscal = str(date_invoice)[0:-4]
            period_fiscal = datetime.strptime(date_invoice, '%Y-%m-%d')
            period_fiscal = period_fiscal.strftime('%m/%Y')
            period_fiscal = str(period_fiscal)
            self.period_fiscal = period_fiscal

    @api.one
    @api.depends('date_invoice')
    def _get_fiscalyear_from_date(self):
        if self.date_invoice:
            date_invoice = self.date_invoice
            year_fiscal = str(date_invoice)[0:-4]
            period_fiscal = datetime.strptime(date_invoice, '%Y-%m-%d')
            period_fiscal = period_fiscal.strftime('%m/%Y')
            period_fiscal = str(period_fiscal)
            self.year_fiscal = year_fiscal