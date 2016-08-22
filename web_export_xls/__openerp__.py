{
    'name': 'Export Data to Excel',
    'sequence': 5,
    'version': '1.0',
    'summary': 'Export Data to Excel',
    'category': 'Backend',
    'author': 'Bruce',
    'description':
        """
        Chosen list records from list view, click to Export XLS
        """,
    'data': [
        'view/web_export_xls.xml',
    ],
    'depends': [
        'web'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'application': True,
    'price': '0',
    'currency': 'USD',
}