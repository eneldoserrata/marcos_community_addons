# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Daniel Reis (https://launchpad.com/~dreis-pt)
#    Copyright (C) 2016 Stella Fredö completed rewrite it for odoo V10
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

{
    'name': "LDAP mapping for user name and e-mail",
    'version': "10.0.1.0.0",
    'depends': ["auth_ldap"],
    'author': "Daniel Reis, re-write it for Odoo 10 by Stella Fredö in Sweden",
    'license': 'AGPL-3',
    'description': """\
Allows to define the LDAP attributes to use to retrieve user name and e-mail
address. actually V10 already retrieved user name, so we only retrieve the email.

got "mail" attribute for user from the LDAP, so it can be mapped into OpenERP.
one more thing: LDAP filer is (&(objectClass=user)(sAMAccountName=%s)) this allow you
to search through all LDAP folders in a multi company environment.
""",
    'category': "Tools",
    'data': [
        'views/users_ldap_view.xml',
    ],
    'installable': True,
}

