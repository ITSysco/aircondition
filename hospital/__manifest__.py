# -*- coding: utf-8 -*-
{
    'name': "Hospital",

    'summary': "Hospital Managment System",

    'description': """
        Hospital Managment System
    """,

    'author': "Sysco",
    'website': "sysco.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'hospital',
    'sequence': -100,
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/patient.tag.csv',
        'data/ir.sequence.xml',
        'data/patient_tag_data.xml',
        'views/menu.xml',
        'wizard/cancel_wizard_view.xml',
        'views/patient_view.xml',
        'views/patient_tag.xml',
        'views/female_patients.xml',
        'views/appointment_view.xml',
        'views/res_config_settings_views.xml',
        'report/report.xml',
        'report/patient_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'application': True,

    'license': 'LGPL-3', 

    'auto-install': False,
}