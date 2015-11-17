# -*- coding: utf-8 -*-
{
    'name': "Importacion de estados de cuentas",

    'summary': """
        Permite importar los extractos bancarios.
        """,

    'description': """
        Luego de descargar el extracto bancario desde el banco este módulo
        le permitirá importarlo para fines de conciliación.
    """,

    'author': 'Eneldo Serrata - Marcos Organizador de Negocios, SRL.',
    'website': "http://marcos.do",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Localization',
    'version': '1,0',

    # any module necessary for this one to work correctly
    'depends': ['base','account_bank_statement_import'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/bank_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}