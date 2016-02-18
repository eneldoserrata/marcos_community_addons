# -*- encoding: utf-8 -*-
{
  'name': 'Web Gantt (Community)',
  'description': 'OpenERP Web Gantt chart view (Community)',
  'version': '0.1dev',
  'category': 'Hidden',
  'author': 'Stefan Becker',
  'depends': ['web'],
  'data': [
    'views/web_gantt.xml'
  ],
  'qweb': [
    'static/src/xml/*.xml'
  ],
  'auto_install': True
}
