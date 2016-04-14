
{
    'name': 'Dynamic List',
    'version': '1.1',
    'author': 'Surekha Technologies',
    'category': 'Dynamic ListView',
    'website': 'https://www.surekhatech.com',
    'summary': 'Dynamic List',
    'description': """

Dynamic List
============
Dynamic List module is made to show/hide the column(s) on the list/tree view of ODOO. After installing the module a "Select Columns" button will be show to the list view before the pagination.

    """,
    'images': ['images/dynamiclist_homepage.jpg'
    ],
    'depends': ['web'],
    'data': [
    'views/listview_button.xml',
    ],
    'demo': [],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': ['static/src/xml/listview_button_view.xml'],
}

