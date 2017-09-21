from odoo import models, api, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _barcode_scanned = fields.Char("Barcode Scanned", help="Value of the last barcode scanned.", store=False)

    @api.model
    def get_po_to_split_from_barcode(self, datarecord_id, barcode):
        pack_ids = self.browse(datarecord_id).pack_operation_product_ids
        return [pack_id.id for pack_id in pack_ids if pack_id.product_id.barcode == barcode][0]
