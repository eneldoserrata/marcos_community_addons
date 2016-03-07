# -*- coding: utf-8 -*-

from openerp import http
import openerp
import logging
import re

_logger = logging.getLogger(__name__)


def db_filter(dbs, httprequest=None):
    httprequest = httprequest or http.request.httprequest
    db_filter_hdr = httprequest.environ.get('HTTP_X_ODOO_DBFILTER', False)
    h = httprequest.environ.get('HTTP_HOST', '').split(':')[0]
    d, _, r = h.partition('.')
    if d == "www" and r:
        d = r.partition('.')[0]
    r = openerp.tools.config['dbfilter'].replace('%h', h).replace('%d', d)
    dbs = [i for i in dbs if re.match(r, i)]
    _logger.info("xxxxxxxxxxxxxxxxxxxxxxxx Dominio raiz %s".format(db_filter_hdr))
    if not dbs and db_filter_hdr:
        dbs = [db_filter_hdr]
    return dbs

http.db_filter = db_filter
