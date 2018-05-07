# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Product Dimensions",
  "summary"              :  "Provide Product Dimensions Option for  products.",
  "category"             :  "Website",
  "version"              :  "0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "website"              :  "https://store.webkul.com/Odoo.html",
  "description"          :  """https://webkul.com/blog/tag/odoo
    Offer dimension attribute like product height, product length, product width
    and measure unit like weight units of measure and dimension units measure for products.
  """,
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=wk_product_dimensions&version=11.0",
  "depends"              :  ['product'],
  "data"                 :  ['views/views.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "pre_init_hook"        :  "pre_init_check",
}
