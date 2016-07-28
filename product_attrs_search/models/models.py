# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools




class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def name_search(self, name, args=None, operator=u'ilike', limit=100):

        result = super(ProductProduct, self).name_search(name, args=args, operator=operator, limit=limit)

        if not result:
            sql = u""" SELECT "products_attrs"."id" FROM "products_attrs" WHERE "products_attrs"."name" ILIKE {} """.format(u"'%{}%'".format(name))
            self._cr.execute(sql)
            res = self._cr.fetchall()
            ids = set([id[0] for id in res])
            result = self.browse(ids).name_get()

        if not result:
            res = self.search([('barcode','like','%{}%'.format(name))])
            ids = set([rec.id for rec in res])
            result = self.browse(ids).name_get()

        return result

    @api.model
    def create_variant_view(self):
        tools.sql.drop_view_if_exists(self._cr, 'products_attrs')
        self._cr.execute("""
                    CREATE VIEW products_attrs AS (
                        SELECT   "product_product"."id" as id,
                             string_agg("product_attribute_value"."name", ' ') as name
                        FROM     "product_attribute_value_product_product_rel"
                        INNER JOIN "product_product"  ON "product_attribute_value_product_product_rel"."prod_id" = "product_product"."id"
                        INNER JOIN "product_attribute_value"  ON "product_attribute_value_product_product_rel"."att_id" = "product_attribute_value"."id"
                        GROUP BY "product_product"."id"
                    )
                    """)

