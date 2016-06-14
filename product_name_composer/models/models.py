# -*- coding: utf-8 -*-

from openerp import models, fields, api

class NewModule(models.TransientModel):
    _name = 'product.name.composer'

    product = fields.Many2many("composer.product", string="Producto")
    brand = fields.Many2many("composer.brand", string="Marca")
    type = fields.Many2many("composer.type", string="Tipo")
    color = fields.Many2many("composer.color", string="Color")
    uom = fields.Many2many("composer.uom", string="Unidad de medida")


    @api.multi
    def create_name(self):
        product_name = []
        product_name += [p.name for p in self.product]
        product_name += [b.name for b in self.brand]
        product_name += [t.name for t in self.type]
        product_name += [c.name for c in self.color]
        product_name += [u.name for u in self.uom]
        product_composer_name = ""
        for name in product_name:
            product_composer_name += "{} ".format(name)
        product_id = self.env["product.template"].browse(self._context.get("active_id"))
        product_id.write({"name": product_composer_name.strip()})



class ComposerProduct(models.Model):
    _name = "composer.product"

    name = fields.Char()


class ComposerBrand(models.Model):
    _name = "composer.brand"

    name = fields.Char()

class ComposerType(models.Model):
    _name = "composer.type"

    name = fields.Char()

class ComposerColor(models.Model):
    _name = "composer.color"

    name = fields.Char()

class ComposerUom(models.Model):
    _name = "composer.uom"

    name = fields.Char()
