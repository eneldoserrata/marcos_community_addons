# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil import relativedelta
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    @api.multi
    def find_over_due(self):
        current_date = datetime.strptime(fields.Date.context_today(self), DF).date()
        invoice_chart_id =self.env['invoice.chart'].search([])
        if not invoice_chart_id:
            account_ids = self.env['account.invoice'].search([])
            if account_ids:
                invoice_chart = 0; paid_cout = 0; draft_cout=0; awaitng_cunt = 0;
                paid_amt = 0.0; draft_amt = 0.0; awaiting_amt = 0.0;
                for account_id in account_ids:
                    if account_id.date_invoice:
                        current_date = datetime.strptime(account_id.date_invoice, "%Y-%m-%d")
                        month_no = int(account_id.date_invoice[5:7])
                        invoice = account_id
                        if invoice.type == 'out_invoice':
                            select_sql_clause = """SELECT state,COUNT(*) as cnt
                                              ,SUM(amount_total) as sumSales
                                          FROM public.account_invoice where journal_id = %s and date_invoice >= %s and date_invoice <= %s and type = %s
                                         GROUP BY state"""
                            start_date = str(invoice.date_invoice)
                            temp_date  = start_date[:7] + '-01'+ start_date[10:]
                            end_date = str(current_date + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10]
                            params = (1,temp_date,end_date,'out_invoice')
                            self.env.cr.execute(select_sql_clause, params)
                            query_results = self.env.cr.dictfetchall()
                            for query_val in query_results:
                                if query_val['state'] == 'draft':
                                        draft_cout = int(query_val['cnt']) if query_val['cnt'] else 0
                                        draft_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
                                if query_val['state'] == 'open':
                                        awaitng_cunt = int(query_val['cnt']) if query_val['cnt'] else 0
                                        awaiting_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
                                if query_val['state'] == 'paid':
                                        paid_cout = int(query_val['cnt']) if query_val['cnt'] else 0
                                        paid_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
                            invoice_chart = self.env['invoice.chart'].search([('month_no','=', month_no)])
                            if invoice_chart:
                                invoice_chart.write({'draft_count':int(draft_cout), 'paid_count':int(paid_cout),'month_no':month_no,'draft_amt':draft_amt,
                                                    'paid_amt':paid_amt,'invoice_id':invoice.id,'awating_count':int(awaitng_cunt),'awating_payment':awaiting_amt})
                            else:
                                invoice_chart.create({'draft_count':int(draft_cout), 'paid_count':int(paid_cout),'month_no':month_no,'draft_amt':draft_amt,
                                                      'paid_amt':paid_amt,'invoice_id':invoice.id,'awating_count':int(awaitng_cunt),'awating_payment':awaiting_amt})
                        elif invoice.type == 'in_invoice':
                            current_date = datetime.strptime(invoice.date_invoice, "%Y-%m-%d")
                            month_no = int(invoice.date_invoice[5:7])
                            select_sql_clause = """SELECT state,COUNT(*) as cnt
                                                          ,SUM(amount_total) as sumSales
                                                      FROM public.account_invoice where journal_id = %s and date_invoice >= %s and date_invoice <= %s and type ='in_invoice'
                                                     GROUP BY state"""
                            start_date = str(invoice.date_invoice)
                            temp_date  = start_date[:7] + '-01'+ start_date[10:]
                            end_date = str(current_date + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10]
                            params = (2,temp_date,end_date)
                            self.env.cr.execute(select_sql_clause, params)
                            query_results = self.env.cr.dictfetchall()
                            for query_val in query_results:
                                if query_val['state'] == 'draft':
                                        draft_cout = int(query_val['cnt']) if query_val['cnt'] else 0
                                        draft_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
                                if query_val['state'] == 'open':
                                        awaitng_cunt = int(query_val['cnt']) if query_val['cnt'] else 0
                                        awaiting_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
                                if query_val['state'] == 'paid':
                                        paid_cout = int(query_val['cnt']) if query_val['cnt'] else 0
                                        paid_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
                            invoice_chart = self.env['invoice.chart'].search([('month_no','=', month_no)])
                            if invoice_chart:
                                invoice_chart.write({'draft_out_count':int(draft_cout), 'paid_out_count':int(paid_cout),'month_no':month_no,'draft_out_amt':draft_amt,
                                                    'paid_out_amt':paid_amt,'invoice_id':invoice.id,'awating_out_count':int(awaitng_cunt),'awating_out_payment':awaiting_amt})
                            else:
                                invoice_chart.create({'draft_out_count':int(draft_cout), 'paid_out_count':int(paid_cout),'month_no':month_no,'draft_out_amt':draft_amt,
                                                    'paid_out_amt':paid_amt,'invoice_id':invoice.id,'awating_out_count':int(awaitng_cunt),'awating_out_payment':awaiting_amt})
                        if invoice_chart:
                            invoice_chart.invoice_chart()
                            invoice_chart.expense_chart()
                            invoice_chart.cashflow_chart()
                            invoice_chart.profit_loss()
            
    
    # Find the customer invoice and vendor expenses values By Moses I  
    def _find_invoice_values(self,current_date, month_no):
        invoice_chart = 0; paid_cout = 0; draft_cout=0; awaitng_cunt = 0;
        paid_amt = 0.0; draft_amt = 0.0; awaiting_amt = 0.0;
        invoice = self
        if invoice.type == 'out_invoice':
            select_sql_clause = """SELECT state,COUNT(*) as cnt
                                          ,SUM(amount_total) as sumSales
                                      FROM public.account_invoice where journal_id = %s and date_invoice >= %s and date_invoice <= %s and type = %s
                                     GROUP BY state"""
            start_date = str(invoice.date_invoice)
            temp_date  = start_date[:7] + '-01'+ start_date[10:]
            end_date = str(current_date + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10]
            params = (1,temp_date,end_date,'out_invoice')
            self.env.cr.execute(select_sql_clause, params)
            query_results = self.env.cr.dictfetchall()
            for query_val in query_results:
                if query_val['state'] == 'draft':
                        draft_cout = int(query_val['cnt']) if query_val['cnt'] else 0
                        draft_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
                if query_val['state'] == 'open':
                        awaitng_cunt = int(query_val['cnt']) if query_val['cnt'] else 0
                        awaiting_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
                if query_val['state'] == 'paid':
                        paid_cout = int(query_val['cnt']) if query_val['cnt'] else 0
                        paid_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
            invoice_chart = self.env['invoice.chart'].search([('month_no','=', month_no)])
            if invoice_chart:
                invoice_chart.write({'draft_count':int(draft_cout), 'paid_count':int(paid_cout),'month_no':month_no,'draft_amt':draft_amt,
                                    'paid_amt':paid_amt,'invoice_id':invoice.id,'awating_count':int(awaitng_cunt),'awating_payment':awaiting_amt})
            else:
                invoice_chart.create({'draft_count':int(draft_cout), 'paid_count':int(paid_cout),'month_no':month_no,'draft_amt':draft_amt,
                                      'paid_amt':paid_amt,'invoice_id':invoice.id,'awating_count':int(awaitng_cunt),'awating_payment':awaiting_amt})
        elif invoice.type == 'in_invoice':
            current_date = datetime.strptime(invoice.date_invoice, "%Y-%m-%d")
            month_no = int(invoice.date_invoice[5:7])
            select_sql_clause = """SELECT state,COUNT(*) as cnt
                                          ,SUM(amount_total) as sumSales
                                      FROM public.account_invoice where journal_id = %s and date_invoice >= %s and date_invoice <= %s and type ='in_invoice'
                                     GROUP BY state"""
            start_date = str(invoice.date_invoice)
            temp_date  = start_date[:7] + '-01'+ start_date[10:]
            end_date = str(current_date + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10]
            params = (2,temp_date,end_date)
            self.env.cr.execute(select_sql_clause, params)
            query_results = self.env.cr.dictfetchall()
            for query_val in query_results:
                if query_val['state'] == 'draft':
                        draft_cout = int(query_val['cnt']) if query_val['cnt'] else 0
                        draft_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
                if query_val['state'] == 'open':
                        awaitng_cunt = int(query_val['cnt']) if query_val['cnt'] else 0
                        awaiting_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
                if query_val['state'] == 'paid':
                        paid_cout = int(query_val['cnt']) if query_val['cnt'] else 0
                        paid_amt = query_val['sumsales'] if query_val['sumsales'] else 0.0
            invoice_chart = self.env['invoice.chart'].search([('month_no','=', month_no)])
            if invoice_chart:
                invoice_chart.write({'draft_out_count':int(draft_cout), 'paid_out_count':int(paid_cout),'month_no':month_no,'draft_out_amt':draft_amt,
                                    'paid_out_amt':paid_amt,'invoice_id':invoice.id,'awating_out_count':int(awaitng_cunt),'awating_out_payment':awaiting_amt})
            else:
                invoice_chart.create({'draft_out_count':int(draft_cout), 'paid_out_count':int(paid_cout),'month_no':month_no,'draft_out_amt':draft_amt,
                                    'paid_out_amt':paid_amt,'invoice_id':invoice.id,'awating_out_count':int(awaitng_cunt),'awating_out_payment':awaiting_amt})
        if invoice_chart:
            if invoice.type == 'out_invoice':
                invoice_chart.invoice_chart()
            if invoice.type == 'in_invoice':
                invoice_chart.expense_chart()
                
    @api.multi
    def action_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: inv.state not in ['proforma2', 'draft']):
            raise UserError(_("Invoice must be in draft or Pro-forma state in order to validate it."))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        # Added function By susai
        if not self.date_invoice:
            self.date_invoice = datetime.strptime(fields.Date.context_today(self), DF)
        current_date = datetime.strptime(self.date_invoice, "%Y-%m-%d")
        month_no = int(self.date_invoice[5:7])
        self._find_invoice_values(current_date, month_no)
        self.env['invoice.chart'].cashflow_chart()
        return to_open_invoices.invoice_validate()
    
       
    @api.multi
    def _write(self, vals):
        pre_not_reconciled = self.filtered(lambda invoice: not invoice.reconciled)
        pre_reconciled = self - pre_not_reconciled
        res = super(AccountInvoice, self)._write(vals)
        reconciled = self.filtered(lambda invoice: invoice.reconciled)
        not_reconciled = self - reconciled
        (reconciled & pre_reconciled).filtered(lambda invoice: invoice.state == 'open').action_invoice_paid()
        (not_reconciled & pre_not_reconciled).filtered(lambda invoice: invoice.state == 'paid').action_invoice_re_open()
        # Added function By Moses I
        if not self.date_invoice:
            self.date_invoice = datetime.strptime(fields.Date.context_today(self), DF)
        current_date = datetime.strptime(self.date_invoice, "%Y-%m-%d")
        month_no = int(self.date_invoice[5:7])
        if vals:
            self._find_invoice_values(current_date,month_no)
        return res