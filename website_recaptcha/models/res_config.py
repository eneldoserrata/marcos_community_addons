from openerp.osv import fields, osv


class website_config_settings(osv.osv_memory):
    _inherit = 'website.config.settings'

    _columns = {
        'recaptcha_site_key': fields.related(
            'website_id', 'recaptcha_site_key', type="char",
            string='reCAPTCHA site Key'),
        'recaptcha_private_key': fields.related(
            'website_id', 'recaptcha_private_key', type="char",
            string='reCAPTCHA Private Key'),
    }

