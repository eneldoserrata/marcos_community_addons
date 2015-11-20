# -*- coding: utf-8 -*-

from openerp import models, api


class PrintCheck(models.AbstractModel):
    _name = 'report.l10n_do_check_printing.check_one'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('l10n_do_check_printing.check_one')

        payment_ids = self.env[report.model].browse(self._ids)

        payments = []
        for payment in payment_ids:
            payment.payment_date
            year, month, day = payment.payment_date.split("-")
            payment.report_date = "{} {} {} {} {} {} {} {}".format(day[0],day[1],month[0],month[1],year[0],year[1],
                                                                   year[2], year[3])
            payments.append(payment)

        docargs = {
            "doc_ids": self._ids,
            "doc_model": report.model,
            "docs": payments
        }
        return report_obj.render('l10n_do_check_printing.check_one', docargs)


