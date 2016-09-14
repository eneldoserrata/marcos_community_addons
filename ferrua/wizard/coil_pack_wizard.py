# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions


class CoilPackWizard(models.TransientModel):
    _name = 'coil.pack.wizard'

    name = fields.Char("Conduce")
    pickin_id = fields.Many2one("stock.picking")
    line_ids = fields.One2many("coil.pack.detail.wizard", "master_id")

    @api.multi
    def empacar(self):
        for rec in self:
            coil_packing = []
            for line in rec.line_ids:
                if line.remaining != 0:
                    raise exceptions.Warning(
                        u"La cantidad restante para el lote {} del producto {} debe ser igual a 0.".format(
                            line.lot_id.name, line.product_id.name))

                for coil in [0,1,2]:
                    if coil == 0 and line.coil_qty_a > 0 and line.label_in_coin_qty_a > 0:
                        coil_packing.append((0, False, {"product_id": line.product_id.id,
                                                        "position": line.position,
                                                        "lot_id": line.lot_id.id,
                                                        "coil_qty": line.coil_qty_a,
                                                        "label_in_coin_qty": line.label_in_coin_qty_a}))
                    elif coil == 1 and line.coil_qty_b > 0 and line.label_in_coin_qty_b > 0:
                        coil_packing.append((0, False, {"product_id": line.product_id.id,
                                                        "position": line.position,
                                                        "lot_id": line.lot_id.id,
                                                        "coil_qty": line.coil_qty_b,
                                                        "label_in_coin_qty": line.label_in_coin_qty_b}))
                    elif coil == 2 and line.coil_qty_c > 0 and line.label_in_coin_qty_c > 0:
                        coil_packing.append((0, False, {"product_id": line.product_id.id,
                                                        "position": line.position,
                                                        "lot_id": line.lot_id.id,
                                                        "coil_qty": line.coil_qty_c,
                                                        "label_in_coin_qty": line.label_in_coin_qty_c}))

            coil_pack_ids = {"coil_pack_ids": coil_packing}
            picking = self.env["stock.picking"].browse(self._context.get("active_id"))
            return picking.put_in_pack(coil_pack_ids=coil_pack_ids)



class CoilPackDetailWizard(models.TransientModel):
    _name = 'coil.pack.detail.wizard'

    @api.one
    @api.depends("coil_qty_a", "coil_qty_b", "coil_qty_c", "label_in_coin_qty_a", "label_in_coin_qty_b",
                 "label_in_coin_qty_c")
    def _remaining_labels(self):
        self.remaining = self.qty - (
            (self.coil_qty_a * self.label_in_coin_qty_a) + (self.coil_qty_b * self.label_in_coin_qty_b) + (
                self.coil_qty_c * self.label_in_coin_qty_c))

    master_id = fields.Many2one("coil.pack.wizard")
    product_id = fields.Many2one("product.product", readonly=True)
    lot_id = fields.Many2one("stock.production.lot", readonly=True)
    position = fields.Integer(string=u'Posición')
    qty = fields.Float("Cantidad", readonly=True)
    coil_qty_a = fields.Integer(string="B [1]")
    label_in_coin_qty_a = fields.Integer(string="E X B [1]")
    coil_qty_b = fields.Integer(string="B [2]")
    label_in_coin_qty_b = fields.Integer(string="E X B [2]")
    coil_qty_c = fields.Integer(string="B [3]")
    label_in_coin_qty_c = fields.Integer(string="E X B [3]")
    remaining = fields.Integer("Restante", compute="_remaining_labels")
