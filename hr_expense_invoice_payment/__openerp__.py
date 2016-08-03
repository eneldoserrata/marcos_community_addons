# -*- encoding: utf-8 -*-

{
    'name': 'Supplier invoices on HR expenses',
    'version': '1.0.1.0.0',
    'category': 'HR',
    'author': 'ERP Ukraine',
    'website': 'http://erp.co.ua',
    'description': """
Pay Supplier invoice with HR expenses.
""",
    'depends': [
        'hr_expense',
    ],
    'data': [
        'views/hr_expense_expense_view.xml',
    ],
    'installable': True,
}
