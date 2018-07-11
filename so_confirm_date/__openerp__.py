# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    'name': 'Sales Order - Confirm Date',
    'version': '8.0.0.1',
    'category': 'Tools',
    'summary': 'Sales Order - Confirm Date',
    'description': """
##############################################################
          Sales Order - Confirm Date
##############################################################     
    *   This module shows Confirmation Date in Sales Order form view (field already exists by default)
    """,

    'author': 'Linserv AB',
    'contributors': ['Riyaj Pathan <rjpathan19@gmail.com>'],
    'website': 'www.linserv.se/en/',

    'depends': ['sale'],
    'data': [ 
        'views/sale.xml',
    ],

    'application': False,
    'auto_install': False,
    'installable': True,
}
