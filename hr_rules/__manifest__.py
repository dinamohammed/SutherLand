# -*- coding: utf-8 -*-
{
    'name': "HR Rules",

    'summary': """
        Hr rules plus add multiple features to employee.""",

    'description': """
        Add multiple new features to employee screen
        from remaining leaves to age and tax related fields extra, this module works
        with multiple automated actions are added to readme folder (to add them manually).
    """,

    'author': "Egymentors - Dina - Ahmed Salama",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['hr_contract', 'hr_payroll', 'hr_holidays', 'tags__rule'],

    # always loaded
    'data': [
        'data/employee_sequence.xml',
        
        'security/ir.model.access.csv',
        
        'views/hr_payroll_view_changes.xml',
        'views/res_config_custom.xml',
        'views/hr_employee_view_changes.xml',
        'views/provin_city_view.xml',
        'views/allowance_deduction.xml',
        'views/contract_template.xml',
    ],
}
