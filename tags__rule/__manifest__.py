# -*- coding: utf-8 -*-
{
    'name': "Tags_Rule",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll', 'hr_contract'],

    # always loaded
    'data': [
        'data/hr_level_data.xml',
        
        'security/ir.model.access.csv',
        
        'views/hr_employee_view_changes.xml',
        'views/hr_payslip_view_changes.xml',
        'views/hr_contract_view_changes.xml',
        'views/location.xml',
        'views/level.xml',
        'views/contract_type_view.xml',
        'views/status.xml',
    ],
    # only loaded in demonstration mode
}
