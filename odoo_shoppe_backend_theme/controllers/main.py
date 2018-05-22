# -*- coding: utf-8 -*-
import werkzeug
import json
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import ensure_db, Home


class OdooShoppeBackendTheme(http.Controller):

    @http.route('/partners/map', type='http', auth='public', website=True)
    def web_social_feed(self, **kwargs):
        partner_datas = {}
        Partners = request.env['res.partner'].sudo().search([
            ('partner_latitude', '!=', 0.0), ('partner_longitude', '!=', 0.0)])

        for partner in Partners:
            partner_datas.update({
                partner.id: [partner.name.encode('utf8'),
                             "%.6f" % round(partner.partner_latitude, 6),
                             "%.6f" % round(partner.partner_longitude, 6)]
            })

        return request.render(
            "odoo_shoppe_backend_theme.material_osbt_partner_location_map", {
            'partners': json.dumps(partner_datas)})


class OdooShoppAppSwitcher(Home):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        ensure_db()
        if not request.session.uid:
            return werkzeug.utils.redirect('/web/login', 303)
        if kw.get('redirect'):
            return werkzeug.utils.redirect(kw.get('redirect'), 303)

        request.uid = request.session.uid
        context = request.env['ir.http'].webclient_rendering_context()
        if request.session.uid:
            ResUserID = request.env['res.users'].sudo().search([('id', '=', request.session.uid)], limit=1)
            if ResUserID.menu_style == 'apps':
                context = dict(context.copy(),
                               app_background_image=ResUserID.company_id.app_background_image or False,
                               user_id=ResUserID.id,
                               company_id=ResUserID.company_id.id,)
                return request.render('odoo_shoppe_backend_theme.webclient_bootstrap_apps', qcontext=context)
        return request.render('web.webclient_bootstrap', qcontext=context)
