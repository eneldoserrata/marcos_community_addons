# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.report import report_sxw

LINE_FILLER = '*'
INV_LINES_PER_STUB = 9

class report_print_check(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(report_print_check, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'pages': self.get_pages,
        })

    def fill_line(self, amount_str):
        return amount_str and (amount_str+' ').ljust(200, LINE_FILLER) or ''

    def get_pages(self, payment):
        """ Returns the data structure used by the template : a list of dicts containing what to print on pages.
        """
        stub_pages = self.make_stub_pages(payment)
        multi_stub = payment.journal_id.do_check_multi_stub
        pages = []
        for i in range(0, stub_pages != None and len(stub_pages) or 1):
            pages.append({
                'sequence_number': payment.check_number\
                    if (payment.journal_id.check_manual_sequencing and payment.check_number != 0)\
                    else False,
                'payment_date': payment.payment_date,
                'partner_name': payment.partner_id.name,
                'currency': payment.currency_id,
                'amount': payment.amount if i == 0 else 'VOID',
                'amount_in_word': self.fill_line(payment.check_amount_in_words) if i == 0 else 'VOID',
                'memo': payment.communication,
                'stub_cropped': not multi_stub and len(payment.invoice_ids) > INV_LINES_PER_STUB,
                # If the payment does not reference an invoice, there is no stub line to display
                'stub_lines': stub_pages != None and stub_pages[i],
            })
        return pages

    def make_stub_pages(self, payment):
        """ The stub is the summary of paid invoices. It may spill on several pages, in which case only the check on
            first page is valid. This function returns a list of stub lines per page.
        """
        if len(payment.invoice_ids) == 0:
            return None

        multi_stub = payment.journal_id.do_check_multi_stub

        invoices = payment.invoice_ids.sorted(key=lambda r: r.date_due)
        debits = invoices.filtered(lambda r: r.type == 'in_invoice')
        credits = invoices.filtered(lambda r: r.type == 'in_refund')

        # Prepare the stub lines
        if not credits:
            stub_lines = [self.make_stub_line(payment, inv) for inv in invoices]
        else:
            stub_lines = [{'header': True, 'name': "Bills"}]
            stub_lines += [self.make_stub_line(payment, inv) for inv in debits]
            stub_lines += [{'header': True, 'name': "Refunds"}]
            stub_lines += [self.make_stub_line(payment, inv) for inv in credits]

        # Crop the stub lines or split them on multiple pages
        if not multi_stub:
            # If we need to crop the stub, leave place for an ellipsis line
            num_stub_lines = len(stub_lines) > INV_LINES_PER_STUB and INV_LINES_PER_STUB-1 or INV_LINES_PER_STUB
            stub_pages = [stub_lines[:num_stub_lines]]
        else:
            stub_pages = []
            i = 0
            while i < len(stub_lines):
                # Make sure we don't start the credit section at the end of a page
                if len(stub_lines) >= i+INV_LINES_PER_STUB and stub_lines[i+INV_LINES_PER_STUB-1].get('header'):
                    num_stub_lines = INV_LINES_PER_STUB-1 or INV_LINES_PER_STUB
                else:
                    num_stub_lines = INV_LINES_PER_STUB
                stub_pages.append(stub_lines[i:i+num_stub_lines])
                i += num_stub_lines

        return stub_pages

    def make_stub_line(self, payment, invoice):
        """ Return the dict used to display an invoice/refund in the stub
        """
        # Find the account.partial.reconcile which are common to the invoice and the payment
        if invoice.type in ['in_invoice', 'out_refund']:
            invoice_sign = 1
            invoice_payment_reconcile = invoice.move_id.line_ids.mapped('matched_debit_ids').filtered(lambda r: r.debit_move_id in payment.move_line_ids)
        else:
            invoice_sign = -1
            invoice_payment_reconcile = invoice.move_id.line_ids.mapped('matched_credit_ids').filtered(lambda r: r.credit_move_id in payment.move_line_ids)

        if payment.currency_id != payment.journal_id.company_id.currency_id:
            amount_paid = abs(sum(invoice_payment_reconcile.mapped('amount_currency')))
        else:
            amount_paid = abs(sum(invoice_payment_reconcile.mapped('amount')))

        return {
            'due_date': invoice.date_due,
            'number': invoice.reference and invoice.number + ' - ' + invoice.reference or invoice.number,
            'amount_total': invoice_sign * invoice.amount_total,
            'amount_residual': invoice_sign * invoice.residual,
            'amount_paid': invoice_sign * amount_paid,
            'currency': invoice.currency_id,
        }


class print_check_bpde(osv.AbstractModel):
    _name = 'report.l10n_do_check_printing.print_check_bpde'
    _inherit = 'report.abstract_report'
    _template = 'l10n_do_check_printing.print_check_bpde'
    _wrapped_report_class = report_print_check