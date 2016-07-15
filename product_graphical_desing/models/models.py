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


class ResPartner(models.Model):
    _inherit = "res.partner"

    desing_id = fields.One2many("product.graphical.desing", "partner_id", string=u"Diseños")
