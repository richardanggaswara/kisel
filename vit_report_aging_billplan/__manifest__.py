# -*- coding: utf-8 -*-
{
    'name': "vit_report_aging_billplan",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','vit_project_rab','vit_project_billplan','vit_project_billplan_inherit','report_xlsx'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'report/report_aging_billplan.xml',
        'data/paperformat_template.xml',
        'report/report_aging_billplan_xls.xml'
    ],
}