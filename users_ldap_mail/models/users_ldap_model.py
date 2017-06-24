# -*- coding: utf-8 -*-
# 

import ldap
import logging
from ldap.filter import filter_format

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)


class CompanyLDAP(models.Model):
    _inherit = 'res.company.ldap'

    email= fields.Char(string='mail', default='mail', help='user email attribute in LDAP')

    @api.multi
    def get_ldap_dicts(self):
        """
        Retrieve res_company_ldap resources from the database in dictionary
        format.
        :return: ldap configurations
        :rtype: list of dictionaries
        """

        ldaps = self.sudo().search([('ldap_server', '!=', False)], order='sequence')
        res = ldaps.read([
            'id',
            'company',
            'ldap_server',
            'ldap_server_port',
            'ldap_binddn',
            'ldap_password',
            'ldap_filter',
            'ldap_base',
            'user',
            'create_user',
            'ldap_tls',
            'email'
        ])
        return res

    def map_ldap_attributes(self, conf, login, ldap_entry):
        """
        Compose values for a new resource of model res_users,
        based upon the retrieved ldap entry and the LDAP settings.
        :param dict conf: LDAP configuration
        :param login: the new user's login
        :param tuple ldap_entry: single LDAP result (dn, attrs)
        :return: parameters for a new resource of model res_users
        :rtype: dict
        """
        return {
            'name': ldap_entry[1]['cn'][0],
            'email': ldap_entry[1]['mail'][0],
            'login': login,
            'company_id': conf['company'][0],
        }
