# -*- encoding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.addons.web.controllers.main import Home

class Login(Home):
    
    @http.route('/account_dashboard_bokeh/invoice_plot', type='http', auth="public", website=True, multilang=True)
    def web_chart_invoice(self, redirect=None, **kw):
        INVOICE_TEMPLATE = None
        for record in request.env['html.template'].sudo().search([]):
            if record.name == 'Invoice':
                INVOICE_TEMPLATE = record.text_file
        return INVOICE_TEMPLATE
    
    @http.route('/account_dashboard_bokeh/expense_plot', type='http', auth="public", website=True, multilang=True)
    def web_chart_expense(self, redirect=None, **kw):
        EXPENSE_TEMPLATE = None
        for record in request.env['html.template'].sudo().search([('name','=','Expense')],limit=1):
            if record:
                EXPENSE_TEMPLATE = record.text_file
        return EXPENSE_TEMPLATE
    
    @http.route('/account_dashboard_bokeh/cashflow_plot', type='http', auth="public", website=True, multilang=True)
    def web_chart_cashflow(self, redirect=None, **kw):
        CASHFLOW_TEMPLATE = None
        for record in request.env['html.template'].sudo().search([]):
            if record.name == 'Cashflow':
                CASHFLOW_TEMPLATE = record.text_file
        return CASHFLOW_TEMPLATE
    
    @http.route('/account_dashboard_bokeh/profitloss_plot', type='http', auth="public", website=True, multilang=True)
    def web_chart_profitloss(self, redirect=None, **kw):
        PROFIT_TEMPLATE = None
        for record in request.env['html.template'].sudo().search([]):
            if record.name == 'Profit':
                PROFIT_TEMPLATE = record.text_file
        return PROFIT_TEMPLATE
    
#     
