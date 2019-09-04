# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : "Open Academy",
    'summary': """Manage Trainings""",
    'sequence': 15,
    'description': """
        Open Academy module for managing trainings:
            - training courses
            - training sessions
            - attendees registration
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    'depends': ['base', 'board'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        #'templates.xml',
        'views/openacademy_view.xml',
        'views/partner.xml',
        'views/session_board.xml',
        'wizard/add_attendees_wizard_view.xml',
        'report/openacademy_report_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'views/openacademy_view.xml',
    ],

}
