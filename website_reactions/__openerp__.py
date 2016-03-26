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
{
    'name': "Reactions!",

    'summary': """
        Add Facebook like reactions to your blog posts. """,

    'description': """
        Give your readers the opportunity to express how they feel about your
        blog posts. Let them like it, love it, dislike it and more. 
    """,

    'author': "menecio",
    'website': "https://www.menecio.me",
    'category': 'website',
    'version': '0.1.1',

    'depends': ['website_blog'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        #~ 'demo/demo.xml',
    ],
}
