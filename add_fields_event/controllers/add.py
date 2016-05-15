# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class add(osv.osv):

  _inherit = "event.event"

  _columns = {
      'short_description': fields.char('Short Description'),
      'website': fields.char('Website'),
      'info': fields.char('Info'),
      'facebook': fields.char('Facebook'),
      'twitter': fields.char('Twitter'),
      'googleplus': fields.char('Google Plus'),
      'image': fields.binary('Image'),
  }

add()


