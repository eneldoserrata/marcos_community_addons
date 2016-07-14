# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    report_logo = fields.Binary("Logo para reportes", attachment=True,
                                 help="This the image used as logo for any report, if non is uploaded, the company logo will be used by default")


class ResPartner(models.Model):
    _inherit = "res.partner"

    two_currency = fields.Boolean("Imprimir dos monedas")



class customized_so_order(models.Model):
    _inherit = "sale.order"

    @api.multi
    def print_quotation(self):
        """ Method called when print button is clicked
       This Method overrides the one in the original sale module
        """
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self, 'ferrua_report.sale_order')




class professional_templates(models.Model):
    _inherit = ["account.invoice"]


    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
           easily the next step of the workflow
       This Method overrides the one in the original invoice class
        """
        self.ensure_one()
        self.sent = True
        return self.env['report'].get_action(self, 'ferrua_report.report_invoice')


class AccountInvoiceReport(models.AbstractModel):
    _name = 'report.sale.report_sale_order'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('sale.report_sale_order')

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
        }

        return report_obj.render('sale.report_sale_order', docargs)

