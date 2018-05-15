from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_history_ids = fields.One2many(comodel_name='sale.order', compute='_compute_customer_history_ids', readonly=True)

    @api.multi
    @api.depends('order_line.order_id')
    def _compute_customer_history_ids(self):
        for sale in self:
            if sale.partner_id:
                sale.customer_history_ids = self.env['sale.order'].search([('partner_id', '=', sale.partner_id.id)])