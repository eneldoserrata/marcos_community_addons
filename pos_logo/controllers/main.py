import functools
import logging
from datetime import datetime, timedelta
import time
import simplejson
import urlparse
import werkzeug.utils
from werkzeug.exceptions import BadRequest

import openerp
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import db_monodb, ensure_db, set_cookie_and_redirect, login_and_redirect
from openerp.addons.auth_signup.controllers.main import AuthSignupHome as Home
from openerp.modules.registry import RegistryManager
from openerp.tools.translate import _
import openerp.pooler as pooler
_logger = logging.getLogger(__name__)


#----------------------------------------------------------
# Controller
#----------------------------------------------------------
class LockoutSign(openerp.addons.web.controllers.main.Home):
    
    @http.route()
    def web_login(self, *args, **kw):        
        ensure_db() 
        dbname = request.session.db        
        registry = RegistryManager.get(dbname)
        #cr = registry.cursor()
        cr = request.cr
        response = super(LockoutSign, self).web_login(*args, **kw)  
        if response.is_qweb and response.qcontext.has_key('error'):
            error = response.qcontext['error']
            if error:
                if request.httprequest.method == 'POST':
                    old_uid = request.uid
                    company_ids = pooler.get_pool(request.session.db).get('res.company').search(cr, SUPERUSER_ID, [])
                    company = pooler.get_pool(request.session.db).get('res.company').browse(cr, SUPERUSER_ID, company_ids[0])
                    attempt_cnt = company.attempt_cnt
                    unlock_after = company.lockouttime_id.value
                    unlock_after_name = company.lockouttime_id.name
                    uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
                    if uid is False:
                        uloginids = pooler.get_pool(request.session.db).get('res.users').search(cr, SUPERUSER_ID, [('login','=',request.params['login'])])
                        for lid in pooler.get_pool(request.session.db).get('res.users').browse(cr, SUPERUSER_ID, uloginids):
                            if lid.flg_userlocked:
                                if unlock_after==0:
                                    error = 'Your Login is temporarily Locked. Please Contact Administrator to Unlock it.'
                                else:
                                    error = 'Your Login is temporarily Locked. Please try after '+unlock_after_name
                            else:        
                                wronglogin_cnt = lid.wronglogin_cnt and lid.wronglogin_cnt+1 or 1
                                pooler.get_pool(request.session.db).get('res.users').write(cr, SUPERUSER_ID,[lid.id],{'wronglogin_cnt': wronglogin_cnt})
                                if int(lid.wronglogin_cnt)>=int(attempt_cnt):
                                    pooler.get_pool(request.session.db).get('res.users').write(cr, SUPERUSER_ID,[lid.id],{'flg_userlocked': True,'userlocked_datetime':time.strftime('%Y-%m-%d %H:%M:%S')})
                                    if unlock_after==0:
                                        error = 'Your Login is temporarily Locked. Please Contact Administrator to Unlock it.'
                                    else:
                                        error = 'Your Login is temporarily Locked. Please try after '+unlock_after_name
                response.qcontext['error'] = error
        return response
        
# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
