# -*- coding: utf-8 -*-

import StringIO

from openerp import models
from openerp.exceptions import UserError

from ofxparse import OfxParser
from ofxparse.ofxparse import OfxParserException


class InheritedAccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    def validate_ofx(self, file):
        try:
            ofx = OfxParser.parse(file)
        except (TypeError, AttributeError, OfxParserException, ValueError):
            raise UserError("No se pudo interpretar el archivo dado!")
        return ofx

    def _parse_file(self, data_file):
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
                'ref': transaction.id,
                'amount': transaction.amount,
                'unique_import_id': transaction.id,
                'bank_account_id': bank_account_id,
                'partner_id': partner_id,
            }
            total_amt += float(transaction.amount)
            transactions.append(vals_line)

        vals_bank_statement = {
            'name': ofx.account.routing_number,
            'transactions': transactions,
            'balance_start': float(ofx.account.statement.balance) - total_amt,
            'balance_end_real': ofx.account.statement.balance,
        }

        bank_journal_id = self.env["account.journal"].search([('bank_acc_number','=',ofx.account.number)])
        if not bank_journal_id:
            raise UserError(u"Debe espesificar el número de la cuenta del banco en el diario!")

        bank_import_type = bank_journal_id.bank_id.statement_import_type
        currency = ofx.account.statement.currency
        if bank_import_type == "bpdofx":
            currency = "DOP"

        return currency, ofx.account.number, [vals_bank_statement]
