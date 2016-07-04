{
    'name': 'Multiple HR Payslip Confirm',
    'version': '9.0',
    'author': 'OmInfoWay',
    'summary': 'Confirm Multiple HR Payslip at a same time.',
    'category': 'HR',
    'depends': ['hr', 'hr_payroll'],
    'data': [
        'views/hr_payslip_view.xml',
        'wizard/hr_payslip_wiz_view.xml',
    ],
    'description': """
        This Module is For Confirm Multiple HR Payslip...
    """,
    'images': ['static/img/main.png'],
    'auto_install': True,
    'installable': True,
}

