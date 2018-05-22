from openerp import api, fields, models, _
from odoo.exceptions import UserError


# class ResLang(models.Model):
#     _inherit = 'res.lang'
#
#     theme_time_format = fields.Selection([
#         ('LT', 'LT'),
#         ('LTS', 'LTS'),
#         ('L', 'L'),
#         ('l', 'l'),
#         ('LL', 'LL'),
#         ('ll', 'll'),
#         ('LLL', 'LLL'),
#         ('lll', 'lll'),
#         ('LLLL', 'LLLL'),
#         ('llll', 'llll'),
#         ],
#         'Theme Time Format', default="LLLL")


class ThemeResUser(models.Model):
    _inherit = 'res.users'

    @api.multi
    def _get_company_theme(self):
        for res in self:
            if res.company_id.theme_type == 'company_theme':
                res.company_theme = True

    hide_theme_switcher = fields.Boolean("Theme Switcher", default=True)
    company_theme = fields.Boolean(compute="_get_company_theme")
    theme = fields.Selection([
        ('orange', 'Orange'),
        ('gray_black', 'Gray Black'),
        ('white', 'White Gray'),

        ('dark_blue', 'Dark Blue'),
        ('blue', 'Blue'),
        ('grey', 'Grey'),

        ('dark_red', 'Dark Red'),
        ('pink', 'Pink'),
        ('yellow_green', 'Yellow'),

        ],
        'User Theme', default="orange")
    menu_style = fields.Selection([('apps', 'Enterprise Menu'), ('sidemenu', 'Default Odooshoppe Menu')], string="Menu Style", default="sidemenu")

    @api.model
    def create(self, vals):
        company = self.env['res.company'].search([('id', '=', vals.get('company_id'))])
        if company.theme_type == 'company_theme':
            vals.update({'theme': company.theme})
        else:
            vals.update({'theme': vals.get('theme')})
        return super(ThemeResUser, self).create(vals)

    @api.multi
    def write(self, data):
        res = super(ThemeResUser, self).write(data)
        if data.get('theme'):
            self.env['ir.qweb'].clear_caches()
        return res

    @api.multi
    def color_switcher_write(self, theme):
        self.sudo().write({'theme': theme})

    @api.model
    def update_default_theme(self):
        users = self.env['res.users'].search([])
        for user in users.filtered(lambda l: not l.theme):
            if user.company_id.theme_type == 'user_theme':
                user.theme = 'orange'
            else:
                user.theme = user.company_id.theme

    @api.multi
    def get_country_flag(self):
        if self.env.user.partner_id.country_id.image:
            return self.env.user.partner_id.country_id.image
        else:
            return False

    @api.multi
    def get_user_time_format(self):
        # values = {}
        # u_lang = self.env['res.lang'].search([('code', '=', self.env.user.partner_id.lang)])
        # if u_lang:
        #     values.update({'time_format_lang': u_lang.iso_code, 'time_format': u_lang.theme_time_format})
        #     return values
        return False


class ResCompany(models.Model):
    _inherit = 'res.company'

    about_company = fields.Html(string='About')
    theme_type = fields.Selection([('company_theme', 'Based On Company Theme'),
        ('user_theme', 'Based On User Theme')], default="user_theme", string="Theme Type")
    theme = fields.Selection([
        ('orange', 'Orange'),
        ('gray_black', 'Gray Black'),
        ('white', 'White Gray'),

        ('dark_blue', 'Dark Blue'),
        ('blue', 'Blue'),
        ('grey', 'Grey'),

        ('dark_red', 'Dark Red'),
        ('pink', 'Pink'),
        ('yellow_green', 'Yellow'),

        ],
        'Company Theme', default="orange")
    flag_image = fields.Binary("Flag Image")
    flag = fields.Selection([('company_flag', 'Company Flag'), ('user_flag', 'User Flag')], default="company_flag")
    app_background_image = fields.Binary("Enterprise Menu Background Image")
    theme_lables_color = fields.Char("Theme Lable Color")

    @api.multi
    def about_company_data(self):
        user = self.env['res.users'].search([('id', '=', self._uid)])
        company_about = user.company_id.about_company
        return company_about

    @api.multi
    def write(self, data):
        users = self.env['res.users'].search([('company_id', '=', self.id)])
        if data.get('theme_type') == 'user_theme':
            for user in users:
                user.theme = 'orange'
                user.hide_theme_switcher = True
        else:
            for user in users:
                if data.get('theme'):
                    theme = data['theme']
                else:
                    theme = self.theme
                user.theme = theme
                user.hide_theme_switcher = False
        self.env['ir.qweb'].clear_caches()
        return super(ResCompany, self).write(data)
