# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class product_image(osv.Model):
    _name = 'product.image'

    _columns = {
        'name': fields.char('Name'),
        'description': fields.text('Description'),
        'image_alt': fields.text('Image Label'),
        'image': fields.binary('Image'),
        'image_small': fields.binary('Small Image'),
        'product_tmpl_id': fields.many2one('product.template', 'Product'),
    }
product_image()

class product_product(osv.Model):
    _inherit = 'product.product'

    _columns = {
        'images': fields.related('product_tmpl_id', 'images', type="one2many", relation="product.image", string='Images', store=False),
    }
product_product()

class product_template(osv.Model):
    _inherit = 'product.template'
    
    _columns = {
        'images': fields.one2many('product.image', 'product_tmpl_id', string='Images'),
    }
product_template()
