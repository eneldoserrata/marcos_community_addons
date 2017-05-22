# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResCompanyTicket(models.Model):

    _inherit = "res.company"

    next_support_ticket_number = fields.Integer(string="Next Support Ticket Number", default="51976386")
