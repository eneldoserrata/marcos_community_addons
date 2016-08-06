# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
import base64

    # .decodestring(file_data)


class ProductGraphicalDesing(models.Model):
    _name = 'product.graphical.desing'

    name = fields.Char("Arte", required=True)
    product_id = fields.Many2one("product.template", string="Producto", require=True)
    partner_id = fields.Many2one("res.partner", string="Cliente", require=True)
    desing = fields.Binary(u"Diseño", require=True)
    note = fields.Text(u"Descripción")
    state = fields.Selection([('old','Descatalogado'),('new','Activo')], default="old", string="Estado")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    desing_id = fields.One2many("product.graphical.desing", "product_id", u"Diseños")
    description_sale = fields.Text('Sale Description', translate=False,
                                    help="A description of the Product that you want to communicate to your customers. "
                                         "This description will be copied to every Sale Order, Delivery Order and Customer Invoice/Refund")
    description_purchase = fields.Text('Purchase Description', translate=False,
                                        help="A description of the Product that you want to communicate to your vendors. "
                                             "This description will be copied to every Purchase Order, Receipt and Vendor Bill/Refund.")
    description_picking = fields.Text('Description on Picking', translate=False)
    # @api.multi
    # def write(self, vals):
    #     if "description_sale" in vals:
    #         if vals["description_sale"] == False:
    #             vals.update({"description_sale":" "})
    #     return super(ProductTemplate, self).write(vals)


class ResPartner(models.Model):
    _inherit = "res.partner"

    desing_id = fields.One2many("product.graphical.desing", "partner_id", string=u"Diseños")
