# -*- coding: utf-8 -*-



from openerp.osv import fields, osv

class add_blog(osv.osv):
    _inherit = "blog.post"

    _columns = {
        'description': fields.text('Description'),
    }

add_blog()





