from odoo import models, fields, api


class PackOperation(models.Model):
    _inherit = 'stock.pack.operation'

    _barcode_scanned = fields.Char("Barcode Scanned", help="Value of the last barcode scanned.", store=False)
    product_barcode = fields.Char(related='product_id.barcode')