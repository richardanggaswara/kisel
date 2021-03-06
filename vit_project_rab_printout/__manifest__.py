# -*- coding: utf-8 -*-
{
    'name': "vit_project_rab_printout",

    'summary': """
        Printout Report RAB pada Project""",

    'description': """
        Printout Report RAB pada Project
    """,

    'author': "Richard Angga",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','vit_project_rab','vit_project_rab_inherit'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'report/project.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}