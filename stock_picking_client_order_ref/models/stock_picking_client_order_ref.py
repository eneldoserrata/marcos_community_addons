# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Roberto Barreiro (<roberto@disgal.es>)
#    All Rights Reserved
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

from openerp.osv import fields, osv

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    _columns = {
        'client_order_ref': fields.char('Reference/Description', copy=True),
        }

class stock_move(osv.osv):
    _inherit = 'stock.move'

    def _picking_assign(self, cr, uid, move_ids, context=None):

        res = super(stock_move, self)._picking_assign(cr, uid, move_ids, context=context)

        move = self.browse(cr, uid, move_ids, context=context)[0]

        # Get the client order ref
        order_obj = self.pool.get("sale.order")
        order_id = order_obj.search(cr, uid, [('name','=', move.origin)], context=context)
        vals = order_obj.read(cr, uid, order_id, ['client_order_ref'])
        for value in vals:
            if value.has_key('client_order_ref'):
                order_ref = value['client_order_ref']
        if order_ref:
            stock_pick_obj = self.pool.get("stock.picking")
            stock_pick_id = stock_pick_obj.search(cr, uid, [('origin', '=', move.origin)], context=context)
            stock_pick_obj.write(cr, uid, stock_pick_id, {'client_order_ref': order_ref}, context=context)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
