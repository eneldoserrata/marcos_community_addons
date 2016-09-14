# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _

import operator


class stock_move(models.Model):
    _inherit = "stock.pack.operation"

    position = fields.Integer(string=u'Posición')

    @api.model
    def create(self, vals):

        picking = self.env["stock.picking"].browse(vals.get("picking_id", False))

        order = False
        if picking.group_id.name:
            order = self.env["sale.order"].search([('name', '=', picking.group_id.name)])

        product_id = vals.get("product_id", False)
        if order:
            for line in order.order_line:
                if line.product_id.id == product_id:
                    vals.update({"position": line.position})
                    break

        return super(stock_move, self).create(vals)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.one
    def _get_client_order_ref(self):
        res = "No aplica"
        if self.group_id:
            order = self.env["sale.order"].search([('name','=',self.group_id.name)])
            if order:
                res = order.client_order_ref
        self.client_order_ref = res

    client_order_ref = fields.Char(compute=_get_client_order_ref)

    def get_coil_report_data(self):
        report_data = {}
        coil_ids = []
        for line in self.pack_operation_product_ids:
            if line.result_package_id:
                for coil in line.result_package_id.coil_pack_ids:
                    if not coil.id in coil_ids:
                        if not report_data.get(line.result_package_id.name, False):
                            report_data.update({line.result_package_id.name: {"lines": [{"position": coil.position,
                                                                                         "product_id": coil.product_id.name,
                                                                                         "lot_id": coil.lot_id.name,
                                                                                         "coil_qty": coil.coil_qty,
                                                                                         "label_in_coin_qty": '{:20,.2f}'.format(coil.label_in_coin_qty),
                                                                                         "labels_total": '{:20,.2f}'.format(coil.labels_total)
                                                                                         }],
                                                                              "total": coil.labels_total}})
                        else:
                            report_data[line.result_package_id.name]["lines"].append({"position": coil.position,
                                                                                      "product_id": coil.product_id.name,
                                                                                      "lot_id": coil.lot_id.name,
                                                                                      "coil_qty": coil.coil_qty,
                                                                                      "label_in_coin_qty": '{:20,.2f}'.format(coil.label_in_coin_qty),
                                                                                      "labels_total": '{:20,.2f}'.format(coil.labels_total)
                                                                                      })
                            report_data[line.result_package_id.name]["total"] += coil.labels_total
                    coil_ids.append(coil.id)


        report_data_list = []
        for pack in report_data:
            report_data[pack]["total"] = '{:20,.2f}'.format(report_data[pack]["total"])
            report_data_list.append(
                {"name": pack, "lines": sorted(report_data[pack]["lines"], key=lambda k: k['position']),
                 "total": report_data[pack]["total"]})
        return sorted(report_data_list, key=lambda k: k['name'])

    def open_coil_packing(self):
        operations = [x for x in self.pack_operation_ids if x.qty_done > 0 and (not x.result_package_id)]
        if not operations:
            raise exceptions.Warning("No hay productos realizados para empacar.")
        pack_operation_ids = []

        for operation in operations:
            for pack in operation.pack_lot_ids:
                pack_operation_ids.append((0, False, {"product_id": operation.product_id.id,
                                                      "lot_id": pack.lot_id.id,
                                                      "qty": pack.qty,
                                                      "position": operation.position
                                                      }))

        res_id = self.env["coil.pack.wizard"].create({"name": self.name,
                                                      "pickin_id": self.id,
                                                      "line_ids": pack_operation_ids})

        return {
            'name': u'Especificación de bobinas',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'coil.pack.wizard',
            'view_id': False,
            'target': 'new',
            'views': False,
            'type': 'ir.actions.act_window',
            "res_id": res_id.id,
            'context': self._context,
        }

    @api.multi
    def put_in_pack(self, context=False, coil_pack_ids={}):
        if not self.location_dest_id.usage == "customer":
            return super(StockPicking, self).put_in_pack()

        if not coil_pack_ids:
            return self.open_coil_packing()
        else:
            stock_operation_obj = self.env["stock.pack.operation"]
            package_obj = self.env["stock.quant.package"]
            package_id = False
            for picking in self:
                operations = [x for x in picking.pack_operation_ids if x.qty_done > 0 and (not x.result_package_id)]
                pack_operation_ids = []
                for operation in operations:
                    op = operation
                    if operation.qty_done < operation.product_qty:
                        new_operation = operation.copy({'product_qty': operation.qty_done,
                                                        'qty_done': operation.qty_done})

                        operation.write({'product_qty': operation.product_qty - operation.qty_done,
                                         'qty_done': 0})
                        if operation.pack_lot_ids:
                            packlots_transfer = [(4, x.id) for x in operation.pack_lot_ids]
                            new_operation.write({'pack_lot_ids': packlots_transfer})

                        op = new_operation
                    pack_operation_ids.append(op.id)
                if operations:
                    stock_operation_obj.browse(pack_operation_ids).check_tracking()
                    package_id = package_obj.create(coil_pack_ids)
                    stock_operation_obj.browse(pack_operation_ids).write({'result_package_id': package_id.id})
                else:
                    raise exceptions.UserError(_('Please process some quantities to put in the pack first!'))
            return package_id


class stock_package(models.Model):
    _inherit = "stock.quant.package"

    coil_pack_ids = fields.One2many("coil.pack", "pack_id")


class CoilPack(models.Model):
    _name = "coil.pack"

    @api.depends("coil_qty", "label_in_coin_qty")
    @api.one
    def _labels_total(self):
        self.labels_total = self.coil_qty * self.label_in_coin_qty

    pack_id = fields.Many2one("stock.quant.package", string="Lote")
    position = fields.Integer(string=u'Posición')
    product_id = fields.Many2one("product.product", string="Producto")
    lot_id = fields.Many2one("stock.production.lot")
    coil_qty = fields.Integer(string="Bobina")
    label_in_coin_qty = fields.Integer(string="Etiquetas por bobinas")
    labels_total = fields.Integer("Total de etiquetas", compute=_labels_total)



