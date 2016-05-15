# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
import requests
import json


class website(osv.osv):
    _inherit = 'website'

    _columns = {
        'recaptcha_site_key': fields.char('reCAPTCHA Site Key'),
        'recaptcha_private_key': fields.char('reCAPTCHA Private Key'),
    }


    def is_captcha_valid(self, cr, uid, ids, response, context={}):
        for website in self.browse(cr, uid, ids, context=context):
            get_res = {'secret': website.recaptcha_private_key,'response': response}
            try:
                response = requests.get('https://www.google.com/recaptcha/api/siteverify', params=get_res)
            except Exception as e:
                raise osv.except_osv(('Invalid Data!'),("%s.")%(e))
            res_con = json.loads(response.content)
            if res_con.has_key('success') and res_con['success']:
                return True
        return False
    
    _defaults = {
                 'recaptcha_site_key': "6LchkgATAAAAAAdTJ_RCvTRL7_TTcN3Zm_YXB39s",
                 'recaptcha_private_key': "6LchkgATAAAAADbGqMvbRxHbTnTEkavjw1gSwCng"
                 }