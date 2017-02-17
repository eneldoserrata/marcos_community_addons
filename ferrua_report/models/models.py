# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

import decimal


class ResCompany(models.Model):
    _inherit = "res.company"

    report_logo = fields.Binary("Logo para reportes", attachment=True,
                                 help="This the image used as logo for any report, if non is uploaded, the company logo will be used by default")


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
        qty = round(decimal.Decimal(self.product_uom_qty),3)
        return "{}".format(qty, 0 if qty == qty else 2)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_date_assign(self):
        if self.payment_term_id.print_currency_id:
            if self.currency_id.id != self.payment_term_id.print_currency_id.id:
                raise exceptions.ValidationError(
                        u"Debe de cambiar la moneda de la factura antes porque la factura esta configurada para ser validada en {}.".format(self.payment_term_id.print_currency_id.name))

        return super(AccountInvoice, self).action_date_assign()

    def render_report_payment_term_note(self):
        if self.rate == self.env.user.company_id.currency_id:
            impuesto = '{0:,.2f}'.format(self.amount_tax)
        else:
            impuesto = '{0:,.2f}'.format(self.amount_tax*self.rate)

        return self.payment_term_id.note.format(
            tasa        = self.rate,
            fecha       = self.date_invoice,
            vence       = self.date_due,
            cliente     = self.partner_id.name,
            numero      = self.number,
            subtotal    = '{0:,.2f}'.format(self.amount_untaxed),
            impuesto    = impuesto,
            total       = '{0:,.2f}'.format(self.amount_total)
        )

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

    @api.multi
    @api.depends("invoice_line_tax_ids", "price_subtotal")
    def _get_itbis_only(self):
        for rec in self:
            if rec.invoice_id.journal_id.purchase_type == "informal":
                for tax in rec.invoice_line_tax_ids:
                    if tax.purchase_tax_type == "itbis":
                        rec.itbis_amount = round(rec.price_subtotal * (tax.amount / 100), 2)

    itbis_amount = fields.Monetary("Itbis", compute=_get_itbis_only)

    def format_qty(self):
        qty = round(decimal.Decimal(self.quantity),3)
        return "{}".format(qty, 0 if qty == qty else 2)


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    def _get_rate(self, rate_date):
        if self.currency_id:

            self._cr.execute("""SELECT rate FROM res_currency_rate
                               WHERE currency_id = %s
                                 AND name = %s
                                 AND (company_id is null
                                     OR company_id = %s)
                            ORDER BY company_id, name desc LIMIT 1""",
                           (self.currency_id.id, rate_date, self.env.user.company_id.id))
            if self._cr.rowcount > 0:
                return (1 / self._cr.fetchone()[0])

            return False

    def _get_currency_domain(self):
        return [('id','!=',self.env.user.company_id.currency_id.id)]

    print_currency_id = fields.Many2one("res.currency", require=True, string=u"Debe facturarse en")
    currency_id = fields.Many2one("res.currency", require=True, string=u"Segunda moneda en la impresión")
    invoice_report_type = fields.Boolean(u"Imprime dos monedas en la factura")
    note = fields.Html(string='Description on the Invoice', translate=True, sanitize=False)
