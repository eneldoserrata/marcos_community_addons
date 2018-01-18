# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
import calendar
from bokeh.charts import Bar
import pandas as pd
from bokeh.charts.attributes import  CatAttr
from bokeh.resources import CDN
from bokeh.embed import file_html

order_months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

class InvoiceChart(models.Model):
    _name = 'invoice.chart'
    
    draft_amt = fields.Float('Draft')
    draft_count = fields.Integer('Draft Count')
    paid_amt = fields.Float('Paid')
    paid_count = fields.Integer('Paid Count')
    awating_payment = fields.Float('Awaiting Payment')
    awating_count = fields.Integer('Awaiting Count')
    overdue_amt = fields.Float('Overdue')
    overdue_count = fields.Integer('Overdue Count')
    #out invoice
    draft_out_amt = fields.Float('Draft')
    draft_out_count = fields.Integer('Draft Count')
    paid_out_amt = fields.Float('Paid')
    paid_out_count = fields.Integer('Paid Count')
    awating_out_payment = fields.Float('Awaiting Payment')
    awating_out_count = fields.Integer('Awaiting Count')
    overdue_out_amt = fields.Float('Overdue')
    overdue_out_count = fields.Integer('Overdue Count')
    invoice_id = fields.Many2one('account.invioce', 'Invoice')
    month_no = fields.Integer('Month NO')
    tota_expenses_per_month = fields.Float('Total Expenses')
    
    def invoice_chart(self):
        actual_list =[];actual_list1 =[];actual_list2 =[]
        for offset in range(0, 13):
            if offset:
                month_name =calendar.month_name[offset]
                invoice_chart_id = self.search([('month_no','=',offset)])
                actual_list.append((month_name[:3],invoice_chart_id.draft_amt,'Draft'))
                actual_list1.append((month_name[:3],invoice_chart_id.awating_payment,'Open'))
                actual_list2.append((month_name[:3],invoice_chart_id.paid_amt,'Paid'))
        full = actual_list + actual_list1+actual_list2
        acctual_amt_list=[];acctual_month_list=[];acctual_state_list=[]
        for ac_mo_sorted in order_months:
            for com_dict in full:
                month , amt, state = com_dict
                if month == ac_mo_sorted:
                    if state == 'Paid':
                        acctual_amt_list.append(amt)
                        acctual_month_list.append(month)
                        acctual_state_list.append(state)
                if month == ac_mo_sorted:
                    if state == 'Open':
                        acctual_amt_list.append(amt)
                        acctual_month_list.append(month)
                        acctual_state_list.append(state)
                if month == ac_mo_sorted:
                    if state == 'Draft':
                        acctual_amt_list.append(amt)
                        acctual_month_list.append(month)
                        acctual_state_list.append(state)
        data = pd.DataFrame({'Group' :acctual_month_list,
            'Year'  :acctual_state_list,
             'Height':acctual_amt_list})
        col = [('red'),('blue'),('green')]
        fig = Bar(data,title=" Receivable Invoices",color=col, values='Height',group='Year', legend='top_right',plot_width=600,
                  plot_height=350,xlabel="Months", ylabel="Values", tools=TOOLS,logo=None,
                  label=CatAttr(columns=['Group'], sort=False),tooltips=[('Month:', '@Group'), ('Value:', '@height')])
        fig.legend.label_text_font_size = "8pt"
        fig.legend.label_height = -10
        fig.legend.glyph_width = 10
        fig.legend.glyph_height = 10
        html = file_html(fig, CDN, "invoices plot")
        template_id = self.env['html.template'].search([('name','=','Invoice')],limit=1)
        if template_id:
                template_id.write({'text_file':html})
                
    
    def expense_chart(self):
        actual_list =[];actual_list1 =[];actual_list2 =[]
        for offset in range(0, 13):
            if offset:
                month_name =calendar.month_name[offset]
                invoice_chart_id = self.search([('month_no','=',offset)])
                actual_list.append((month_name[:3],invoice_chart_id.draft_out_amt,'Draft'))
                actual_list1.append((month_name[:3],invoice_chart_id.awating_out_payment,'Open'))
                actual_list2.append((month_name[:3],invoice_chart_id.paid_out_amt,'Paid'))
                full = actual_list + actual_list1+actual_list2
                acctual_amt_list=[];acctual_month_list=[];acctual_state_list=[]
        for ac_mo_sorted in order_months:
            for com_dict in full:
                month , amt, state = com_dict
                if month == ac_mo_sorted:
                    if state == 'Paid':
                        acctual_amt_list.append(amt)
                        acctual_month_list.append(month)
                        acctual_state_list.append(state)
                if month == ac_mo_sorted:
                    if state == 'Open':
                        acctual_amt_list.append(amt)
                        acctual_month_list.append(month)
                        acctual_state_list.append(state)
                if month == ac_mo_sorted:
                    if state == 'Draft':
                        acctual_amt_list.append(amt)
                        acctual_month_list.append(month)
                        acctual_state_list.append(state)
        data = pd.DataFrame({'Group' :acctual_month_list,
            'Year'  :acctual_state_list,
             'Height':acctual_amt_list})
        col = [('red'),('blue'),('green')]
        fig = Bar(data,title="Payable Invoices",color=col, values='Height',group='Year', legend='top_right',plot_width=600,
                  plot_height=350,xlabel="Months", ylabel="Values", tools=TOOLS,logo=None,
                  label=CatAttr(columns=['Group'], sort=False),tooltips=[('Month:', '@Group'), ('Value:', '@height')])
        fig.legend.label_text_font_size = "8pt"
        fig.legend.label_height = -10
        fig.legend.glyph_width = 10
        fig.legend.glyph_height = 10
        html = file_html(fig, CDN, "invoices plot")
        template_id = self.env['html.template'].search([('name','=','Expense')],limit=1)
        if template_id:
            template_id.write({'text_file':html})
                
                
    def cashflow_chart(self):
        actual_list =[];actual_list1 =[];actual_list2 =[]
        for offset in range(0, 13):
            if offset:
                name =calendar.month_name[offset]
                invoice_chart_id = self.search([('month_no','=',offset)])
                actual_list.append((name[:3],invoice_chart_id.awating_payment,'Incoming'))
                actual_list1.append((name[:3],invoice_chart_id.awating_out_payment,'Outgoing'))
        full = actual_list + actual_list1+actual_list2
        acctual_amt_list=[];acctual_month_list=[];acctual_state_list=[]
        for ac_mo_sorted in order_months:
            for com_dict in full:
                month , amt, state = com_dict
                if month == ac_mo_sorted:
                    if state == 'Incoming':
                        acctual_amt_list.append(amt)
                        acctual_month_list.append(month)
                        acctual_state_list.append(state)
                if month == ac_mo_sorted:
                    if state == 'Outgoing':
                        acctual_amt_list.append(amt)
                        acctual_month_list.append(month)
                        acctual_state_list.append(state)
        col = [('green'),('darkred')]
        data = pd.DataFrame({'Group' :acctual_month_list,
                    'Year'  :acctual_state_list,
                     'Height':acctual_amt_list})
        fig = Bar(data,title="CashFlow", values='Height',group='Year',color=col, legend='top_right',plot_width=600,
                  plot_height=350,xlabel="Months", ylabel="Values", tools=TOOLS,logo=None,
                  label=CatAttr(columns=['Group'], sort=False),tooltips=[('Month:', '@Group'), ('Value:', '@height')])
        fig.legend.label_text_font_size = "8pt"
        fig.legend.label_height = -10
        fig.legend.glyph_width = 10
        fig.legend.glyph_height = 10 
        html = file_html(fig, CDN, "cashflow plot")
        template_id = self.env['html.template'].search([('name','=','Cashflow')],limit=1)
        if template_id:
                template_id.write({'text_file':html})
    
    def profit_loss(self):
        actual_list =[];actual_list1 =[];
        for offset in range(0, 13):
            if offset:
                invoice_chart_id = self.search([('month_no','=',offset)])
                name =calendar.month_name[offset]
                actual_list.append((name[:3],invoice_chart_id.paid_amt,'Profit'))
                actual_list1.append((name[:3],invoice_chart_id.paid_out_amt,'Loss'))
        full = actual_list + actual_list1
        acctual_amt_list=[];acctual_month_list=[];acctual_state_list=[]
        for ac_mo_sorted in order_months:
            for com_dict in full:
                month , amt, state = com_dict
                if month == ac_mo_sorted:
                    if state == 'Profit':
                        acctual_amt_list.append(amt)
                        acctual_month_list.append(month)
                        acctual_state_list.append(state)
                if month == ac_mo_sorted:
                    if state == 'Loss':
                        acctual_amt_list.append(amt)
                        acctual_month_list.append(month)
                        acctual_state_list.append(state)
        data = pd.DataFrame({'Group' :acctual_month_list,
                    'Year'  :acctual_state_list,
                     'Height':acctual_amt_list})
        fig = Bar(data,title="Profit & Loss", values='Height',group='Year', legend='top_right',plot_width=600,
                  plot_height=350,xlabel="Months", ylabel="Values", tools=TOOLS,logo=None,
                  label=CatAttr(columns=['Group'], sort=False),tooltips=[('Month:', '@Group'), ('Value:', '@height')])
        fig.legend.label_text_font_size = "8pt"
        fig.legend.label_height = -10
        fig.legend.glyph_width = 10
        fig.legend.glyph_height = 10
        html = file_html(fig, CDN, "cashflow plot")
        template_id = self.env['html.template'].search([('name','=','Profit')],limit=1)
        if template_id:
                template_id.write({'text_file':html})
        
class HtmlTemplate(models.Model):
    _name = 'html.template' 
    
    name = fields.Char('Name')
    template_name = fields.Html('Template Name')
    text_file = fields.Text('Text')

