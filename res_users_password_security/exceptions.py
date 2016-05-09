# -*- coding: utf-8 -*-
# © 2015-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.exceptions import Warning as UserError


class PassError(UserError):
    """ Example: When you try to create an insecure password."""
    def __init__(self, msg):
        self.message = msg
        super(PassError, self).__init__(msg)
