# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import time

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp
import openerp.addons.product.product
import base64

_logger = logging.getLogger(__name__)

class pos_config(osv.osv):
    _inherit = 'pos.config'    
    
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
        

        
    
    def _get_default_image(self, cr, uid, context=None):
        image_path = openerp.modules.get_module_resource('pos_logo', 'static/src/img', 'default.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))       
        
        
    _columns = {
        'image': fields.binary("Logo",
            		help="This field holds the image, limited to 1024x1024px."),
	'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            	string="Medium-sized photo", type="binary", multi="_get_image",
            	     store = {
                	'pos.config': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            	},
            	     help="Medium-sized photo of the student. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
	'image_small': fields.function(_get_image, fnct_inv=_set_image,
		    string="Small-sized photo", type="binary", multi="_get_image",
		    store = {
		        'pos.config': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
		    },
		    help="Small-sized photo of the employee. It is automatically "\
		         "resized as a 64x64px image, with aspect ratio preserved. "\
		         "Use this field anywhere a small image is required."),
        'time_format':fields.selection([('12','12 Hour Format'),('24','24 Hour Format')],'Time Format'),
        'auto_location':fields.char('Auto Location'),
    }
    _defaults={
        'image':_get_default_image,
        'time_format':'24',
    }
    
    
    
    
    
    
    
    
    
    

