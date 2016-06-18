# -*- coding: utf-8 -*-

from openerp import models, fields, api

class NewModule(models.TransientModel):
    _name = 'product.name.composer'


    partner = fields.Many2many("composer.partner", string="Cliente")
    type = fields.Many2many("composer.type", string="Tipo")
    product = fields.Many2many("composer.product", string="Nombre")
    brand = fields.Many2many("composer.brand", string="Linea")
    size = fields.Many2many("composer.size", string="Medida")
    uom = fields.Many2many("composer.uom", string="Unidad")


    @api.multi
    def create_name(self):
        product_name = []
        product_name += [p.name for p in self.partner]
        product_name += [t.name for t in self.type]
        product_name += [p.name for p in self.product]
        product_name += [b.name for b in self.brand]
        product_name += [c.name for c in self.size]
        product_name += [u.name for u in self.uom]
        product_composer_name = u""
        for name in product_name:
            product_composer_name += u"{} ".format(name)
        product_id = self.env["product.template"].browse(self._context.get("active_id"))
        product_id.write({"name": product_composer_name.strip()})


class ComposerPartner(models.Model):
    _name = "composer.partner"

    name = fields.Char()


class ComposerType(models.Model):
    _name = "composer.type"

    name = fields.Char()


class ComposerProduct(models.Model):
    _name = "composer.product"

    name = fields.Char()


class ComposerBrand(models.Model):
    _name = "composer.brand"

    name = fields.Char()

class ComposerSize(models.Model):
    _name = "composer.size"

    name = fields.Char()

class ComposerUom(models.Model):
    _name = "composer.uom"

    name = fields.Char()
