# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ResCountryState(models.Model):
    _inherit = "res.country.state"

    city = fields.Char("Ciudad")
    code = fields.Char('State Code', size=5, help='The state code in max. five chars.', required=True)


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