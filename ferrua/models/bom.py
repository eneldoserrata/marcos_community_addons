# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, u"{} - Cantidad: {} - Unidad: {}".format(rec.product_id.name, rec.product_qty, rec.product_uom.name)))

        return result

    @api.multi
    @api.depends("sustrato","NO_DE_ETIQUETAS","ETIQUETAS_A_TRAVES","REPITE","ETIQUETAS_AL_REDEDOR")
    def _compute_producer(self):
        for rec in self:

            rec.ANCHO_BANDA = 1
            rec.LARGO = 1
            rec.LAMINADO_ANCHO_BANDA = 1
            rec.LAMINADO_LARGO = 1
            if rec.sustrato:
                for attr in rec.sustrato.attribute_value_ids:
                    if attr.attribute_id.name == "Banda":
                        rec.ANCHO_BANDA = float(attr.name)
                    if attr.attribute_id.name == "Largo":
                        rec.LARGO = (float(attr.name)*12)/10

            if rec.laminado:
                for attr in rec.laminado.attribute_value_ids:
                    if attr.attribute_id.name == "Banda":
                        rec.LAMINADO_ANCHO_BANDA = float(attr.name)
                    if attr.attribute_id.name == "Largo":
                        rec.LAMINADO_LARGO = (float(attr.name)*12)/10

            CANTIDAD = rec.product_uom._compute_qty(rec.product_uom.id, rec.product_qty, rec.product_id.uom_id.id)
            rec.ETIQUETAS_A_TRAVES = 1 if rec.ETIQUETAS_A_TRAVES <= 0 else rec.ETIQUETAS_A_TRAVES
            rec.REPITE = 1 if rec.REPITE <= 0 else rec.REPITE
            rec.ETIQUETAS_AL_REDEDOR = 1 if rec.ETIQUETAS_AL_REDEDOR <= 0 else rec.ETIQUETAS_AL_REDEDOR
            rec.CONTEO_A_IMPRIMIR = 1 if rec.CONTEO_A_IMPRIMIR <= 0 else rec.CONTEO_A_IMPRIMIR
            rec.NO_DE_ETIQUETAS = 1 if rec.NO_DE_ETIQUETAS <= 0 else rec.NO_DE_ETIQUETAS
            rec.LARGO = 1 if rec.LARGO <= 0 else rec.LARGO


            rec.CONTEO_A_IMPRIMIR = CANTIDAD/(rec.ETIQUETAS_A_TRAVES*(10/(rec.REPITE/rec.ETIQUETAS_AL_REDEDOR)))

            rec.sustrato_roll = ((rec.CONTEO_A_IMPRIMIR+1200)/rec.LARGO)

            if rec.LAMINADO_LARGO > 1:
                rec.laminado_roll = (rec.CONTEO_A_IMPRIMIR/rec.LAMINADO_LARGO)
            else:
                rec.laminado_roll = 0

            rec.NO_DE_REBOBINADO = rec.NO_DE_ETIQUETAS/(10/(rec.REPITE/rec.ETIQUETAS_AL_REDEDOR))

            rec.ROLLOS_DOBLES = rec.NO_DE_REBOBINADO/2
            rec.ROLLOS_TRIPLES = rec.NO_DE_REBOBINADO/3

            rec.TOTAL_DE_ROLLOS = CANTIDAD/rec.NO_DE_ETIQUETAS

            rec.cilinder_station_1 = rec.REPITE*8
            rec.cilinder_station_2 = rec.REPITE*8
            rec.cilinder_station_3 = rec.REPITE*8
            rec.cilinder_station_4 = rec.REPITE*8
            rec.cilinder_station_5 = rec.REPITE*8
            rec.cilinder_station_6 = rec.REPITE*8
            rec.cilinder_station_7 = rec.REPITE*8
            rec.cilinder_station_8 = rec.REPITE*8

    @api.onchange("sustrato","laminado_roll")
    def onchange_calc(self):
        self._compute_producer()

    arte_id = fields.Many2one("product.graphical.desing", string="Codigo del Arte")
    arte_img = fields.Binary(related="arte_id.desing")

    sustrato_roll = fields.Float(compute=_compute_producer)
    laminado_roll = fields.Float(compute=_compute_producer)
    ANCHO_BANDA = fields.Float(compute=_compute_producer)
    LARGO = fields.Float(compute=_compute_producer)
    LAMINADO_ANCHO_BANDA = fields.Float(compute=_compute_producer)
    LAMINADO_LARGO = fields.Float(compute=_compute_producer)
    REPITE = fields.Float(default=1)

    CUCHILLAS_REMOVIBLES = fields.Boolean()
    TROQUELADO = fields.Many2many("product.product", domain=[('categ_id','=',8)])
    CANTIDAD_DE_ROLLOS = fields.Integer(default=1)
    CORTE_LINEAL = fields.Boolean()
    ETIQUETAS_A_TRAVES = fields.Integer(default=1)
    HOJEADO = fields.Boolean()
    ETIQUETAS_AL_REDEDOR = fields.Integer(default=1)

    NO_DE_REBOBINADO = fields.Integer(compute=_compute_producer)
    NO_DE_ETIQUETAS = fields.Integer(default=1)
    CONTEO_A_IMPRIMIR = fields.Integer(compute=_compute_producer)
    TOTAL_DE_ROLLOS = fields.Float(compute=_compute_producer)
    ROLLOS_DOBLES = fields.Integer(compute=_compute_producer)
    ROLLOS_TRIPLES = fields.Integer(compute=_compute_producer)

    rew = fields.Many2one("img.rew")
    img = fields.Binary(related="rew.img")

    sustrato = fields.Many2one("product.product", domain=[('categ_id','in',(13,14))])
    laminado = fields.Many2one("product.product", domain=[('categ_id','=',10)])
    color_station_1 = fields.Many2one("product.product", string="Color Estacion 1", domain=[('categ_id','in',(9,11,12,15))])
    color_station_2 = fields.Many2one("product.product", string="Color Estacion 2", domain=[('categ_id','in',(9,11,12,15))])
    color_station_3 = fields.Many2one("product.product", string="Color Estacion 3", domain=[('categ_id','in',(9,11,12,15))])
    color_station_4 = fields.Many2one("product.product", string="Color Estacion 4", domain=[('categ_id','in',(9,11,12,15))])
    color_station_5 = fields.Many2one("product.product", string="Color Estacion 5", domain=[('categ_id','in',(9,11,12,15))])
    color_station_6 = fields.Many2one("product.product", string="Color Estacion 6", domain=[('categ_id','in',(9,11,12,15))])
    color_station_7 = fields.Many2one("product.product", string="Color Estacion 7", domain=[('categ_id','in',(9,11,12,15))])
    color_station_8 = fields.Many2one("product.product", string="Color Estacion 8", domain=[('categ_id','in',(9,11,12,15))])

    anilox_station_1 = fields.Char("Anilox Estacion 1")
    anilox_station_2 = fields.Char("Anilox Estacion 2")
    anilox_station_3 = fields.Char("Anilox Estacion 3")
    anilox_station_4 = fields.Char("Anilox Estacion 4")
    anilox_station_5 = fields.Char("Anilox Estacion 5")
    anilox_station_6 = fields.Char("Anilox Estacion 6")
    anilox_station_7 = fields.Char("Anilox Estacion 7")
    anilox_station_8 = fields.Char("Anilox Estacion 8")

    cilinder_station_1 = fields.Integer("Cilindro Estacion 1", compute=_compute_producer)
    cilinder_station_2 = fields.Integer("Cilindro Estacion 2", compute=_compute_producer)
    cilinder_station_3 = fields.Integer("Cilindro Estacion 3", compute=_compute_producer)
    cilinder_station_4 = fields.Integer("Cilindro Estacion 4", compute=_compute_producer)
    cilinder_station_5 = fields.Integer("Cilindro Estacion 5", compute=_compute_producer)
    cilinder_station_6 = fields.Integer("Cilindro Estacion 6", compute=_compute_producer)
    cilinder_station_7 = fields.Integer("Cilindro Estacion 7", compute=_compute_producer)
    cilinder_station_8 = fields.Integer("Cilindro Estacion 8", compute=_compute_producer)

    note = fields.Text("Notas")

    attribute_value_ids = fields.Many2many(related="product_id.attribute_value_ids")
    
    
    @api.model
    def create(self, vals):
        res = super(MrpBom, self).create(vals)
        self.update_component_list()
        return res

    @api.multi
    def write(self, vals):
        res = super(MrpBom, self).write(vals)
        self.update_component_list()
        return res

    def update_component_list(self):
        bom_line = self.env["mrp.bom.line"]

        bom_line.search([("bom_id",'=',self.id)]).unlink()

        if self.sustrato:
            bom_line.create({"bom_id": self.id, "product_id": self.sustrato.id, "product_qty": self.sustrato_roll})

        if self.laminado:
            bom_line.create({"bom_id": self.id, "product_id": self.laminado.id, "product_qty": self.laminado_roll})

        if self.color_station_1:
            bom_line.create({"bom_id": self.id, "product_id": self.color_station_1.id, "product_qty": 1})

        if self.color_station_2:
            bom_line.create({"bom_id": self.id, "product_id": self.color_station_2.id, "product_qty": 1})

        if self.color_station_3:
            bom_line.create({"bom_id": self.id, "product_id": self.color_station_3.id, "product_qty": 1})

        if self.color_station_4:
            bom_line.create({"bom_id": self.id, "product_id": self.color_station_4.id, "product_qty": 1})

        if self.color_station_5:
            bom_line.create({"bom_id": self.id, "product_id": self.color_station_5.id, "product_qty": 1})

        if self.color_station_6:
            bom_line.create({"bom_id": self.id, "product_id": self.color_station_6.id, "product_qty": 1})

        if self.color_station_7:
            bom_line.create({"bom_id": self.id, "product_id": self.color_station_7.id, "product_qty": 1})

        if self.color_station_8:
            bom_line.create({"bom_id": self.id, "product_id": self.color_station_8.id, "product_qty": 1})
        

class RewImg(models.Model):
    _name = "img.rew"

    name = fields.Integer()
    img = fields.Binary()


class mrp_bom(models.Model):
    _inherit = 'mrp.production'

    qty_available = fields.Float(related="product_id.qty_available", string="Cantidad en inventario")