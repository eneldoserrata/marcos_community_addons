# -*- coding: utf-8 -*-

from openerp import http
import openerp

import re


def db_filter(dbs, httprequest=None):
    httprequest = httprequest or http.request.httprequest
    db_filter_hdr = httprequest.environ.get('HTTP_X_ODOO_DBFILTER', False)
    h = httprequest.environ.get('HTTP_HOST', '').split(':')[0]
    d, _, r = h.partition('.')
    if d == "www" and r:
        d = r.partition('.')[0]
    r = openerp.tools.config['dbfilter'].replace('%h', h).replace('%d', d)
    dbs = [i for i in dbs if re.match(r, i)]
    if not dbs and db_filter_hdr:
        dbs = [db_filter_hdr]
    return dbs

http.db_filter = db_filter