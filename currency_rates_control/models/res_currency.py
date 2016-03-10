# -*- coding: utf-8 -*-

# NOTE: this code write by Alexis de Lattre <alexis.delattre@akretion.com> on odoo module Currency Rate Date Check


from openerp import models, fields
from openerp.exceptions import Warning


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def _get_current_rate(
            self, cr, uid, ids, raise_on_no_rate=True, context=None):
        if context is None:
            context = {}
        # We don't check if we don't have 'date' in context, which is
        # a pb because it means Odoo can do a rate conversion
        # on today's date with an old rate, but otherwize it would raise
        # too often, for example it would raise entering the
        # Currencies menu entry !
        if context.get('date') and not context.get('disable_rate_date_check'):
            date = context.get('date')
            for currency_id in ids:
                # We could get the company from the currency, but it's not a
                # 'required' field, so we should probably continue to get it
                # from the user, shouldn't we ?
                user = self.pool['res.users'].browse(cr, uid, uid,
                                                     context=context)
                # if it's the company currency, don't do anything
                # (there is just one old rate at 1.0)
                if user.company_id.currency_id.id == currency_id:
                    continue
                else:
                    # now we do the real work !
                    cr.execute(
                        'SELECT rate, name FROM res_currency_rate '
                        'WHERE currency_id = %s '
                        'AND name <= %s '
                        'ORDER BY name desc LIMIT 1',
                        (currency_id, date))
                    if cr.rowcount:
                        rate_date = cr.fetchone()[1]
                        rate_date_dt = fields.Datetime.from_string(rate_date)
                        date_dt = fields.Datetime.from_string(date)
                        max_delta = user.company_id.currency_rate_max_delta
                        if (date_dt - rate_date_dt).days > max_delta:
                            currency = self.browse(
                                cr, uid, currency_id, context=context)
                            raise Warning(
                                _('You are requesting a rate conversion on %s '
                                  'for currency %s but the nearest '
                                  'rate before that date is '
                                  'dated %s and the maximum currency '
                                  'rate time delta for '
                                  'your company is %s days')
                                % (date, currency.name, rate_date, max_delta))
        # Now we call the regular function from the "base" module
        return super(ResCurrency, self)._get_current_rate(
            cr, uid, ids, raise_on_no_rate=raise_on_no_rate, context=context)