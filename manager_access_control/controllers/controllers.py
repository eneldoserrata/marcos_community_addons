# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import Database



class Database(Database):

    @http.route('/web/database/manager', type='http', auth="user")
    def manager(self, **kw):
        if not request.env.user or request.env.user.id != 1:
            return False
        return self._render_template()

    @http.route('/web/database/selector', type='http', auth="none")
    def selector(self, **kw):
        if not request.env.user or request.env.user.id != 1:
            return False
        return self._render_template(manage=False)