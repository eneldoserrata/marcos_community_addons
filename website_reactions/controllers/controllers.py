# -*- coding: utf-8 -*-
#    Copyright (C) 2016  Aristobulo Meneses <me@menecio.me>
#    
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
import werkzeug

from openerp import http
from openerp.addons.web.http import request
from openerp.addons.website.models.website import slug


class WebsiteReactions(http.Controller):
    @http.route(
        '/blog/<model("blog.blog"):blog>/post/<model("blog.post"):blog_post>/'
        'react/<string:reaction>', 
        auth='user', website=False)
    def react(self, blog, blog_post, reaction, **kw):
        env = request.env
        user_reaction = env['post.reaction'].search([
            ('user_id', '=', env.user.id),
            ('post_id', '=', blog_post.id),
        ])
        if user_reaction:
            user_reaction.sudo().write({'reaction': reaction})
        else:
            env['post.reaction'].sudo().create({
                'post_id': blog_post.id,
                'user_id': env.user.id,
                'reaction': reaction,
            })
        return werkzeug.utils.redirect('/blog/%s/post/%s#reactions' % 
            (slug(blog), slug(blog_post)))
