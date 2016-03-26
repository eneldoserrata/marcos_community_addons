#! -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Rui Pedrosa Franco All Rights Reserved
#    http://pt.linkedin.com/in/ruipedrosafranco
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import datetime


import logging
_logger = logging.getLogger(__name__)

class ir_module_module(models.Model):
    
    _inherit = 'ir.module.module'

    #let's create a field to hold the date of the last time someone pressed the button "updated"
    dt_date_updated = fields.Datetime('Latest update', 
                                      help='This is the last time the module was deliberately installed/updated.')

    
    def dt_dummy(self, cr, uid, module_id):
        if module_id:
            self.button_immediate_upgrade(cr, uid, module_id, {})
        else:
            return True

    
    def set_dt_date_updated(self, cr, uid, module_id):
        self.write(cr, uid, module_id, {'dt_date_updated' : datetime.datetime.now()})

    
        """
        When a module is updated from within the dependencies list, the last module to be updated is the "outside" one.
        This way, we get to set as last updated the one we actually clicked on.
        """
        module_res = self.browse(cr, uid, module_id)
    
        #Let's change the menu name and the associated action
        model_data_obj = self.pool.get('ir.model.data')
        model_ids = model_data_obj.search(cr, uid, [('name','=','menu_update_module')]) # the menu's id
        if model_ids:
            model_res = model_data_obj.browse(cr, uid, model_ids)

            menu_name="[ REUPDATE: %s ]" % (module_res['name'] or 'x')
            menu_obj=self.pool.get('ir.ui.menu')
            menu_obj.write(cr, uid, model_res['res_id'], {'name' : menu_name})

            menu_res=menu_obj.browse(cr, uid, model_res['res_id'])
                    
            action_code = "self.pool.get('ir.module.module').dt_dummy(cr, uid, %s)" % (module_id)
            self.pool.get('ir.actions.server').write(cr, uid, menu_res['action'].id, {'code' : action_code})
        
        return True


    def _button_immediate_function(self, cr, uid, ids, function, context=None):
        
        if isinstance(ids,(list,tuple)):
            ids=ids[0]
        
        self.set_dt_date_updated(cr, uid, ids)
 
        return super(ir_module_module, self)._button_immediate_function(cr, uid, [ids], function, context=context)        



    def module_uninstall(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'dt_date_updated': False})
        return super(ir_module_module, self).module_uninstall(cr, uid, ids, context=context)



class module_dependency(models.Model):
    
    _inherit = 'ir.module.module.dependency'
    
    
    @api.one
    def dt_button_install(self):
        module_obj = self.pool.get('ir.module.module')
        module_id = module_obj.search(self._cr, self._uid, [('name','=',self.name)])
        module_obj._button_immediate_function(self._cr, self._uid, module_id, module_obj.button_install)
        return True

    @api.one
    def dt_button_immediate_upgrade(self):
        module_obj=self.pool.get('ir.module.module')
        module_id=module_obj.search(self._cr, self._uid, [('name','=',self.name)])
        module_obj._button_immediate_function(self._cr, self._uid, module_id, module_obj.button_upgrade)
        return True

    @api.one
    def dt_button_uninstall(self):
        module_obj=self.pool.get('ir.module.module')
        module_id=module_obj.search(self._cr, self._uid, [('name','=',self.name)])
        module_obj.module_uninstall(self._cr, self._uid, module_id, {})
        return True
