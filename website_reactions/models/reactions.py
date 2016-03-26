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


from openerp import models, fields, api, _


class PostReaction(models.Model):
    _name = 'post.reaction'
    
    user_id = fields.Many2one('res.users', 'User', select=1, required=True)
    post_id = fields.Many2one('blog.post', 'Post', select=1, required=True)
    reaction = fields.Selection([
        ('like', _('Like')),
        ('love', _('Love it')),
        ('haha', _('Ha Ha!')),
        ('sad', _('Sad')),
        ('wow', _('WOW')),
        ('angry', _('Angry')),
        ('dislike', _('Dislike'))], 'Reaction', required=True)


    @api.multi
    def reactions_per_post(self):
        res = {}
        posts = [r.post_id.id for r in self]
        for pid in posts:
            # initialise reaction count per post
            res[pid] = {
                'like': 0,
                'love': 0,
                'haha': 0,
                'sad': 0,
                'wow': 0,
                'angry': 0,
                'dislike': 0,
            }
        for rec in self:
            res[rec.post_id.id][rec.reaction] += 1
        return res
