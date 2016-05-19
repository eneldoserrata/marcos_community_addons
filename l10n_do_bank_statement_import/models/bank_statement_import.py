# -*- coding: utf-8 -*-

import StringIO

from openerp import models, _
from openerp.exceptions import UserError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

from ofxparse import OfxParser
from ofxparse.ofxparse import OfxParserException
from openerp.addons.base.res.res_bank import sanitize_account_number

from babel.dates import format_date

class InheritedAccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    def validate_ofx(self, file):
        try:
            ofx = OfxParser.parse(file)
        except (TypeError, AttributeError, OfxParserException, ValueError):
            raise UserError("No se pudo interpretar el archivo dado!")
        return ofx

    def _parse_file(self, data_file):
        locale = self._context.get('lang', 'en_US')
        ofx = self.validate_ofx(StringIO.StringIO(data_file))

        transactions = []
        total_amt = 0.00
        for transaction in ofx.account.statement.transactions:
            bank_account_id = partner_id = False
            partner_bank = self.env['res.partner.bank'].search([('partner_id.name', '=', transaction.payee)], limit=1)
            if partner_bank:
                bank_account_id = partner_bank.id
                partner_id = partner_bank.partner_id.id
            vals_line = {
                'date': transaction.date,
                'name': transaction.payee + (transaction.memo and ': ' + transaction.memo or ''),
                'ref': u"{}: {}".format(int(transaction.id)-1, format_date(transaction.date, 'EEEE d', locale=locale)),
                'amount': transaction.amount,
                'unique_import_id': "{}-{}".format(transaction.id, transaction.date.strftime(DEFAULT_SERVER_DATE_FORMAT)),
                'bank_account_id': bank_account_id,
                'partner_id': partner_id,
            }
            total_amt += float(transaction.amount)
            transactions.append(vals_line)

        dates = [st.date for st in ofx.account.statement.transactions]
        min_date = min(dates)
        max_date = max(dates)
        vals_bank_statement = {
            'name': "Del {} al {} de {}".format(min_date.strftime("%d"), max_date.strftime("%d"), format_date(max_date, 'MMMM', locale=locale)),
            'transactions': transactions,
            'balance_start': float(ofx.account.statement.balance) - total_amt,
            'balance_end_real': ofx.account.statement.balance,
            'date': max_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        }

        bank_journal_id = self.env["account.journal"].search([('bank_acc_number','=',ofx.account.number)])
        if not bank_journal_id:
            raise UserError(u"Debe espesificar el número de la cuenta del banco en el diario!")

        bank_import_type = bank_journal_id.bank_id.statement_import_type
        currency = ofx.account.statement.currency
        if bank_import_type == "bpdofx":
            currency = "DOP"

        return currency, ofx.account.number, [vals_bank_statement]


    def _find_additional_data(self, currency_code, account_number):
        """ Look for a res.currency and account.journal using values extracted from the
            statement and make sure it's consistent.
        """
        company_currency = self.env.user.company_id.currency_id
        journal_obj = self.env['account.journal']
        currency = None
        sanitized_account_number = sanitize_account_number(account_number)

        if currency_code:
            currency = self.env['res.currency'].search([('name', '=ilike', currency_code)], limit=1)
            if not currency:
                raise UserError(_("No currency found matching '%s'.") % currency_code)
            if currency == company_currency:
                currency = False

        journal = journal_obj.browse(self.env.context.get('journal_id', []))
        if account_number:
            # No bank account on the journal : create one from the account number of the statement
            if journal and not journal.bank_account_id:
                journal.set_bank_account(account_number)
            # Already a bank account on the journal : check it's the same as on the statement
            elif journal and journal.bank_account_id.sanitized_acc_number != sanitized_account_number:
                raise UserError(_('The account of this statement (%s) is not the same as the journal (%s).') % (account_number, journal.bank_account_id.acc_number))
            # No journal passed to the wizard : try to find one using the account number of the statement
            elif not journal:
                journal = journal_obj.search([('bank_account_id.sanitized_acc_number', '=', sanitized_account_number)])

        # If importing into an existing journal, its currency must be the same as the bank statement
        if journal:
            journal_currency = journal.currency_id
            if currency is None:
                currency = journal_currency
            # if currency and currency != journal_currency:
            #     statement_cur_code = not currency and company_currency.name or currency.name
            #     journal_cur_code = not journal_currency and company_currency.name or journal_currency.name
            #     raise UserError(_('The currency of the bank statement (%s) is not the same as the currency of the journal (%s) !') % (statement_cur_code, journal_cur_code))

        # If we couldn't find / can't create a journal, everything is lost
        if not journal and not account_number:
            raise UserError(_('Cannot find in which journal import this statement. Please manually select a journal.'))

        return currency, journal
