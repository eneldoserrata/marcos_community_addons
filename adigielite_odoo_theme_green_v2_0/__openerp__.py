{
    'name': 'ADigiElite Odoo 10 Backend-Theme-Green',
    'version': '1.0',
    'author': 'Arun Gnanaraj',
    'description': '''
        Fancy Green backend theme for Odoo 10.
		We do custom theme based on the request. 
		email : arun@adigielite.com
		website : http://www.adigielite.com/
    ''',
    'category': 'Themes/Backend', 
    'depends': [
        'base',
    ],
    'data': [
        'views/custom_view.xml',
    ],
    'images':[
            'static/description/main_screenshot.jpg',
    ],
    'css': ['static/src/css/styles.css'],
    'auto_install': False,
    'installable': True,
}


