from openerp import models, fields, _, api
import logging

_logger = logging.getLogger(__name__)

class PosTable(models.Model):
    _name = "pos.table"

    name = fields.Char('Name', required=1)
    number = fields.Char('Number', required=1)
    company_id = fields.Many2one('res.company', 'Company', readonly=1)
    capacity = fields.Integer('Capacity')
    image = fields.Binary('Image')
    state = fields.Selection([
        ('not_use', 'Not Use'),
        ('used', 'Used'),
        ('order', 'Order')
    ],string='State')
    user_id = fields.Many2one('res.users', 'User Owner')


class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    table_id = fields.Many2one('pos.table', 'Table', readonly=1)

    def _order_fields(self, cr, uid, ui_order, context=None):
        res = super(PosOrder, self)._order_fields(cr, uid, ui_order, context=context)
        if ui_order.has_key('table_id'):
            res.update({
                'table_id': ui_order['table_id']
            })
        return res

    def create_from_ui(self, cr, uid, orders, context=None):
        _logger.info('_______ START create_from_ui _______')
        _logger.info(orders)
        res = super(PosOrder, self).create_from_ui(cr, uid, orders, context=context)
        _logger.info(res)
        _logger.info('_______ END ______')
        return res


class pos_config(models.Model):
    _inherit = "pos.config"
    
    table_ids = fields.Many2many('pos.table', string='Tables')
    kitchen = fields.Boolean('Kitchen POS')


class PosKitchen(models.Model):

    _name = "pos.kitchen"

    name = fields.Char('Name', required=1)
    product_id = fields.Many2one('product.product', 'Product', required=1)
    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='waiting')
    table_id = fields.Many2one('pos.table', 'Table', required=1)
    qty = fields.Float('Quantiry', readonly=1)
    image = fields.Binary(related='product_id.image_small', string='Image')
    uom_id = fields.Many2one('product.uom', 'Uom(s)')

    def create_from_ui(self, cr, uid, orderLine, context={}):
        _logger.info('_____ START create_from_ui_______')
        _logger.info(orderLine)
        _logger.info('total ship: %s' % len(orderLine))
        for lines in orderLine:
            vals = {
                'product_id': lines.get('product_id'),
                'table_id': lines.get('table_id'),
                'name': lines.get('name'),
                'qty': lines.get('qty'),
                'uom_id': lines.get('uom_id')
            }
            self.create(cr, uid, vals)
        _logger.info('_________ END _________')
        return True


