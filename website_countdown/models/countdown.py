# -*- encoding: utf-8 -*-

##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from odoo import api, fields, models

class Countdown(models.AbstractModel):
    _name = 'ir.qweb.field.countdown'
    _inherit = 'ir.qweb.field'


    @api.model
    def record_to_html(self, record, field_name, options=None):
    	return self.env['ir.qweb'].render('website_countdown.countdown', {'countdown_date':record[field_name], 'options':options})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
