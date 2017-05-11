# -*- coding: utf-8 -*-
{
    'name': 'Super Mail',
    'version': '1.1',
    'category': 'Extra Tools',
    'summary': 'Full re-definition of the message_post function to add extra context parameters',
    'description': '''
A technical module to redefine functionality of default message_post
    * Message_post is fully redefined for all the models inherited from mail.thread
    * Several context actions are added to guarantee work of the modules 'internal_thread', 'compoze_no_auto_subscribe', 'super_inbox'
    ''',
    'auto_install': False,
    'application': True,
    'author': 'IT Libertas',
    'website': 'http://itlibertas.com',
    'depends': [
        'mail',
    ],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
            ],
    'qweb': [

            ],
    'js': [

            ],
    'demo': [

            ],
    'test': [

            ],
    'license': 'Other proprietary',
    'images': ['static/description/main.png'],
    'update_xml': [],
    'installable': True,
    'private_category': False,
    'external_dependencies': {
    },
}
