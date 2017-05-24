# -*- coding: utf-8 -*-
{
    'license': 'LGPL-3',
    'name': "Document Thumbnail",
    'summary': "View related document thumbnail",
    'description': """
    """,
    'author': "renjie <i@renjie.me>",
    'website': "https://renjie.me",
    'support': 'i@renjie.me',
    'category': 'Document Management',
    'version': '1.2',
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