# -*- coding: utf-8 -*-

from openerp.addons.web import http
from openerp.http import request


class bizclouds(http.Controller):
    #------------------------------------------------------
    # View
    #------------------------------------------------------

    @http.route('/article', type='http', auth="public", website=True)
    def search(self, page=0, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        article_obj = pool['blog.post']

        domain = []
        if search:
            domain += ['|', '|', ('name', 'ilike', search),
                       ('subtitle', 'ilike', search), ('content', 'ilike', search)]
        article_ids = article_obj.search(cr, uid, domain, context=context)
        articles = article_obj.browse(cr, uid, article_ids, context=context)

        values = {
            'search': search,
            'articles': articles,
            'news': 'active',
        }
        return request.website.render("site_magic3brothers.news", values)

    @http.route('/p/<string:page>', type='http', auth="public", website=True)
    def page(self, page, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        template = 'site_magic3brothers.' + page
        news_obj = pool['blog.post']
        values={
            'aboutus' : 'active' if page == 'aboutus' else '',
            'business': 'active' if page == 'business' else '',
            'culture': 'active' if page == 'culture' else '',
            'news': 'active' if page == 'news' else '',
            'articles': news_obj.browse(cr,uid,news_obj.search(cr,uid,[], limit = 6), context=context) if page == 'news' else '',
        }
        return request.website.render(template, values)

    @http.route('/news/<model("blog.post"):blog_post>', type='http', auth="public", website=True)
    def article(self, blog_post, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        blog_post_obj = request.registry['blog.post']
        # Find next Post
        all_post_ids = blog_post_obj.search(cr, uid, [], context=context)
        # should always return at least the current post
        current_blog_post_index = all_post_ids.index(blog_post.id)
        next_post_id = all_post_ids[0 if current_blog_post_index == len(all_post_ids) - 1 \
                            else current_blog_post_index + 1]
        next_post = next_post_id and blog_post_obj.browse(cr, uid, next_post_id, context=context) or False
        pre_post_id = all_post_ids[len(all_post_ids) - 1 if current_blog_post_index == 0 else current_blog_post_index - 1]
        pre_post = pre_post_id and blog_post_obj.browse(cr, uid, pre_post_id, context=context) or False

        values = {
            'blog_post': blog_post,
            'next_post': next_post,
            'pre_post': pre_post,
        }
        response = request.website.render("site_magic3brothers.article", values)
        return response

