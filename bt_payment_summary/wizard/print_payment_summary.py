# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 BroadTech IT Solutions Pvt Ltd 
#    (<http://broadtech-innovations.com>).
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

from odoo import models, fields, api, _
from odoo.tools.misc import xlwt
import io
import base64
from xlwt import easyxf
import datetime

class PrintPaymentSummary(models.TransientModel):
    _name = "print.payment.summary"
    
    @api.model
    def _get_from_date(self):
        company = self.env.user.company_id
        current_date = datetime.date.today()
        from_date = company.compute_fiscalyear_dates(current_date)['date_from']
        return from_date
    
    from_date = fields.Date(string='From Date', default=_get_from_date)
    to_date = fields.Date(string='To Date', default=fields.Date.context_today)
    payment_summary_file = fields.Binary('Payment Summary Report')
    file_name = fields.Char('File Name')
    payment_report_printed = fields.Boolean('Payment Report Printed')
    currency_id = fields.Many2one('res.currency','Currency', default=lambda self: self.env.user.company_id.currency_id)
    
    
    @api.multi
    def action_print_payment_summary(self,):
        workbook = xlwt.Workbook()
        column_heading_style = easyxf('font:height 200;font:bold True;')
        worksheet = workbook.add_sheet('Payment Summary')
        
        worksheet.write(1, 0, _('Invoice Number'), column_heading_style) 
        worksheet.write(1, 1, _('Customer'), column_heading_style)
        worksheet.write(1, 2, _('Invoice Date'), column_heading_style)
        worksheet.write(1, 3, _('Invoice Amount'), column_heading_style)
        worksheet.write(1, 4, _('Invoice Currency'), column_heading_style)
        worksheet.write(1, 5, _('Paid Amount'), column_heading_style)
        worksheet.col(0).width = 5000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 5000
        worksheet.col(3).width = 5000
        worksheet.col(4).width = 5000
        worksheet.col(5).height = 5000
          
        worksheet2 = workbook.add_sheet('Customer wise Payment Summary')
        worksheet2.write(1, 0, _('Customer'), column_heading_style)
        worksheet2.write(1, 1, _('Paid Amount'), column_heading_style)
        worksheet2.col(0).width = 5000
        worksheet2.col(1).width = 5000
        row = 2
        customer_row = 2
        for wizard in self:
            heading =  'Payment Summary Report (' + str(wizard.currency_id.name) + ')'
            worksheet.write_merge(0, 0, 0, 5, heading, easyxf('font:height 200; align: horiz center;pattern: pattern solid, fore_color black; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            customer_payment_data = {}
            invoice_objs = self.env['account.invoice'].search([('date_invoice','>=',wizard.from_date),
                                                               ('date_invoice','<=',wizard.to_date),
                                                               ('payment_ids','!=',False)])
            for invoice in invoice_objs:
                worksheet.write(row, 0, invoice.number)
                worksheet.write(row, 1, invoice.partner_id.name)
                worksheet.write(row, 2, invoice.date_invoice)
                worksheet.write(row, 3, invoice.amount_total)
                worksheet.write(row, 4, invoice.currency_id.symbol)
                paid_amount = 0
                for payment in invoice.payment_ids:
                    if payment.state != 'draft' and payment.currency_id == wizard.currency_id:
                        paid_amount += payment.amount
                worksheet.write(row, 5, paid_amount)
                if invoice.partner_id.name not in customer_payment_data:
                    customer_payment_data.update({invoice.partner_id.name: paid_amount})
                else:
                    paid_amount_data = customer_payment_data[invoice.partner_id.name] + paid_amount
                    customer_payment_data.update({invoice.partner_id.name: paid_amount_data})
                row += 1
            for customer in customer_payment_data:
                worksheet2.write(customer_row, 0, customer)
                worksheet2.write(customer_row, 1, customer_payment_data[customer])
                customer_row += 1
#             worksheet.write(row, 5, invoice.symbol)
              
            with io.BytesIO() as fp:
                workbook.save(fp)
                excel_file = base64.b64encode(fp.getvalue())
                wizard.payment_summary_file = excel_file
                wizard.file_name = 'Payment Summary Report.xls'
                wizard.payment_report_printed = True
            return {
                    'view_mode': 'form',
                    'res_id': wizard.id,
                    'res_model': 'print.payment.summary',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self.env.context,
                    'target': 'new',
                       }

    
# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
