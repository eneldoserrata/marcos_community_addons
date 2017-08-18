
{
    'name': 'Apps Customize Columns of List (Tree) View',
    'version': '10.0.1.2',
    'author': 'odooapps.cn',
    'category': 'Productivity',
    'website': 'https://www.odooapps.cn',
    'sequence': 2,
    'summary': 'Apps Customize columns of  List (Tree) View. Dynamic list.',
    'description': """

Apps Customize Columns of List (Tree) View
============
Apps Customize Columns of List (Tree) View module is made to show/hide the columns on the list/tree view of Odoo. After installing the module, a "Set Columns" button will be show to the list view.
You can customize every odoo list/tree view easily.

This module is ready for Community and Enterprise Edition.

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

