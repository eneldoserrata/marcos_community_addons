# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class manager_access_control(models.Model):
#     _name = 'manager_access_control.manager_access_control'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100