# -*- coding: utf-8 -*-

from openerp import models, api, _

class account_payment(models.Model):
    _inherit = "account.payment"

    @api.multi
    def do_print_checks(self):
        check_layout = self[0].journal_id.do_check_layout
        if check_layout != 'disabled':
            return self.env['report'].get_action(self, check_layout)
        return super(account_payment, self).do_print_checks()
