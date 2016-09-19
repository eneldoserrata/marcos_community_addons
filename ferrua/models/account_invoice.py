# -*- coding: utf-8 -*-


from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice.line"

    @api.one
    @api.depends("sale_line_ids")
    def _get_picking_name(self):
        if self.sale_line_ids:
            procurement_id = self.env["procurement.order"].search([('sale_line_id','=',self.sale_line_ids.id)])
            if procurement_id:
                stock_move_id = self.env["stock.move"].search([('procurement_id', '=', procurement_id.id)])
                if stock_move_id:
                    picking_names = set()

                    for move in stock_move_id:
                        picking_names.add(move.picking_id.name)

                    self.picking_names = " ".join(picking for picking in picking_names) if picking_names else ""


    picking_names = fields.Char(compute=_get_picking_name, string="Conduce")