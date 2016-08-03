# -*- coding: utf-8 -*-
{
    'license': 'LGPL-3',
    'name': "Document Thumbnail",
    'summary': "view related document thumbnail",
    'description': """
    """,
    'author': "renjie <i@renjie.me>",
    'website': "http://renjie.me",
    'category': 'Document Management',
    'version': '1.0',
    'depends': ['document'],
    'data': [
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/base.xml",
    ],
    'images': [
        'static/description/main_screenshot.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}