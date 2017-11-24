# -*- coding: utf-8 -*-
{
    'name': "auth_signup_name_split",

    'summary': """
        auth_signup_name_split""",

    'description': """
        auth_signup_name_split
    """,

    'author': "UAB Pralo",
    'website': "http://www.pralo.eu",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'auth_signup'],

    'data': [
        'auth_signup_login_inherited.xml',
    ],
}