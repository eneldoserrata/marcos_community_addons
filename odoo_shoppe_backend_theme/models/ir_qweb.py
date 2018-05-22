# # -*- coding: utf-8 -*-
from lxml import etree

from openerp import models, tools
from openerp.http import request
 
from odoo.addons.base.ir.ir_qweb.assetsbundle import AssetsBundle
# from odoo.addons.base.ir.ir_qweb.assetsbundle import StylesheetAsset
from odoo.addons.base.ir.ir_qweb.qweb import QWeb
# 
# class ThemeAssetsBunlde(AssetsBundle):
#     
#     def to_html(self, sep=None, css=True, js=True, debug=False, async=False, url_for=(lambda url: url)):
#         if sep is None:
#             sep = '\n            '
#         response = []
#         if debug == 'assets' or self.name == 'odoo_shoppe_backend_theme.material_osbt_theme_assets':
#             if css and self.stylesheets:
#                 if not self.is_css_preprocessed():
#                     self.preprocess_css(debug=debug)
#                     if self.css_errors:
#                         msg = '\n'.join(self.css_errors)
#                         self.stylesheets.append(StylesheetAsset(self, inline=self.css_message(msg)))
#                 for style in self.stylesheets:
#                     if self.name == 'odoo_shoppe_backend_theme.material_osbt_theme_assets':
#                         import pdb; pdb.set_trace()
#                     response.append(style.to_html())
#             if js:
#                 for jscript in self.javascripts:
#                     response.append(jscript.to_html())
#         else:
#             if css and self.stylesheets:
#                 css_attachments = self.css()
#                 if not self.css_errors:
#                     for attachment in css_attachments:
#                         response.append('<link href="%s" rel="stylesheet"/>' % url_for(attachment.url))
#                 else:
#                     msg = '\n'.join(self.css_errors)
#                     self.stylesheets.append(StylesheetAsset(self, inline=self.css_message(msg)))
#                     for style in self.stylesheets:
#                         response.append(style.to_html())
#             if js and self.javascripts:
#                 response.append('<script %s type="text/javascript" src="%s"></script>' % (async and 'async="async"' or '', url_for(self.js().url)))
#         response.extend(self.remains)
#         return sep + sep.join(response)


class IrQWeb(models.AbstractModel, QWeb):
    _inherit = 'ir.qweb'

    @tools.conditional(
        # in non-xml-debug mode we want assets to be cached forever, and the admin can force a cache clear
        # by restarting the server after updating the source code (or using the "Clear server cache" in debug tools)
        'xml' not in tools.config['dev_mode'],
        tools.ormcache_context('xmlid', 'options.get("lang", "en_US")', 'css', 'js', 'debug', 'async', keys=("website_id",)),
    )
    def _get_asset(self, xmlid, options, css=True, js=True, debug=False, async=False, values=None):
        files, remains = self._get_asset_content(xmlid, options)
        asset = AssetsBundle(xmlid, files, remains, env=self.env)
        if xmlid == 'odoo_shoppe_backend_theme.material_osbt_theme_assets':
            debug = 'assets'
        html_bundel = asset.to_html(css=css, js=js, debug=debug, async=async, url_for=(values or {}).get('url_for', lambda url: url))
        if xmlid == 'odoo_shoppe_backend_theme.material_osbt_theme_assets':
            theme = self.env.user.theme
            material_theme = theme
            if not material_theme:
                material_theme = 'material_default'  # if no theme found means user login first time so set orange one default
            links = []
            for link in html_bundel.split('\n'):
                if link:
                    link = etree.fromstring(link)
                    theme = link.get('href').split('/')[-1][:-9]
                    if material_theme != theme:
                        link.set('disabled', 'true')
                    link.set('theme', theme)
                    link = etree.tostring(link)
                    links.append(link)
            html_bundel = b'\n'.join(links).decode()
        return html_bundel

# # class IrQweb(models.AbstractModel):
# #     _inherit = 'ir.qweb'
# # 
# #     # Ugly hack to stop making assets bundle of theme even in without debug mode and added disabled attributes at init
# #     def render_tag_call_assets(self, element, template_attributes, generated_attributes, qwebcontext):
# #         xmlid = template_attributes['call-assets']
# #         preserve_debug = qwebcontext['debug']
# #         if xmlid == 'odoo_shoppe_backend_theme.material_osbt_theme_assets':
# #             qwebcontext['debug'] = True
# #         html = super(IrQweb, self).render_tag_call_assets(element, template_attributes, generated_attributes, qwebcontext)
# #         if xmlid == 'odoo_shoppe_backend_theme.material_osbt_theme_assets':
# #             material_theme = None
# #             # TODO: so main idea is that client provide theme name and server less to css processpr build
# #             # css from only one theme.less file with @media and @variable that do not required to laod all the theme at client side
# #             # cons: it need to reload webclient after theme change
# #             if 'request' in qwebcontext:
# #                 theme = request.env.user.theme
# #                 material_theme = theme
# #             if not material_theme:
# #                 material_theme = 'material_default'  # if no theme found means user login first time so set orange one default
# #             links = []
# # 
# #             for link in html.split('\n'):
# #                 if link:
# #                     link = etree.fromstring(link)
# #                     theme = link.get('href').split('/')[-1][:-9]
# #                     if material_theme != theme:
# #                         link.set('disabled', 'true')
# #                     link.set('theme', theme)
# #                     link = etree.tostring(link)
# #                     print 'final link', link
# #                     links.append(link)
# #             html = '\n'.join(links)
# #             qwebcontext['debug'] = preserve_debug
# #         return html
