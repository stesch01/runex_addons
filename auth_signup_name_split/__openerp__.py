# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    "name": "Authentication Signup Name Split",
    "version": "1.0",
    "author": "Linserv AB",
    "category": "Authentication",
    "summary": "Authentication Signup Name Split Module",
    "website": "www.linserv.se",
    "contributors": [
        'Gediminas Venclova <gediminasv@live.com>'
    ],
    "license": "",
    "depends": [
        'base', 'auth_signup'
    ],
    'description': """

        Authentication Signup Name Split Module

        This module splits name field into name and surname in signup screen.
    """,
    "demo": [],
    "data": [
        'auth_signup_login_inherited.xml',
    ],
    "test": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    "auto_install": False,
}