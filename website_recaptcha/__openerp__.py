# -*- coding: utf-8 -*-

{'name': 'Website Google reCAPTCHA',
 'category': 'Website',
 'depends': ['website'],
 'author': 'DevTalents',
 'website': 'www.templates-odoo.com',
 'description': """
Odoo Website reCAPTCHA
================================
This modules allows you to integrate Google reCAPTCHA to your website.
You can configure your Google reCAPTCHA site and public keys
""",
 'data': [
          'views/website_view.xml',
          'views/res_config.xml',
 ],
 'installable': True,
}
