# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    report_logo = fields.Binary("Logo para reportes", attachment=True,
                                 help="This the image used as logo for any report, if non is uploaded, the company logo will be used by default")
