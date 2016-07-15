# -*- coding: utf-8 -*-

from openerp import models, fields, api

import decimal


class ResCompany(models.Model):
    _inherit = "res.company"

    report_logo = fields.Binary("Logo para reportes", attachment=True,
                                 help="This the image used as logo for any report, if non is uploaded, the company logo will be used by default")


class ResPartner(models.Model):
    _inherit = "res.partner"

    two_currency = fields.Boolean("Imprimir dos monedas")



class SaleOrder(models.Model):
    _inherit = "sale.order"

    not_total = fields.Boolean("IMPRIMIR SIN TOTAL", default=False)

    @api.multi
    def print_quotation(self):
        """ Method called when print button is clicked
       This Method overrides the one in the original sale module
        """
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self, 'ferrua_report.sale_order')


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def format_qty(self):
        qty = decimal.Decimal(self.product_uom_qty)
        return "{}".format(qty, 0 if qty == qty else 2)



class AccountInvoice(models.Model):
    _inherit = "account.invoice"


    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
           easily the next step of the workflow
       This Method overrides the one in the original invoice class
        """
        self.ensure_one()
        self.sent = True
        return self.env['report'].get_action(self, 'ferrua_report.report_invoice')


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    def format_qty(self):
        qty = decimal.Decimal(self.quantity)
        return "{}".format(qty, 0 if qty == qty else 2)