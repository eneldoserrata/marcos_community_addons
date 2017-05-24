# -*- encoding: utf-8 -*-

from openerp import api, fields, models, _

class base_config_settings(models.TransientModel):
    _inherit = 'base.config.settings'

    @api.model
    def _get_default_birthday_mail_template(self):
        return self.env.user.company_id.birthday_mail_template and self.env.user.company_id.birthday_mail_template.id or False


    birthday_mail_template = fields.Many2one('mail.template', 'Birthday Wishes Template',
        default=_get_default_birthday_mail_template, required=True,
        help='This will set the default mail template for birthday wishes.')

    
    @api.multi
    def set_birthday_mail_template(self):
        if self.birthday_mail_template:
            self.env.user.company_id.write({'birthday_mail_template': self.birthday_mail_template.id})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
 