# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ResCountryState(models.Model):
    _inherit = "res.country.state"

    city = fields.Char("Ciudad")
    code = fields.Char('State Code', size=5, help='The state code in max. five chars.', required=True)


    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        result = super(ResCountryState, self).name_search(name, args=args, operator=operator, limit=limit)

        if not result:
            res = self.search([('city',operator,name)])
            ids = set([id[0] for id in res])
            result = self.browse(ids).name_get()
        if not result:
            res = self.search([('code',operator,name)])
            ids = set([id[0] for id in res])
            result = self.browse(ids).name_get()

        return result



class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id,
                              "city": state.city,
                              "zip": state.code}}
        return {'value': {}}