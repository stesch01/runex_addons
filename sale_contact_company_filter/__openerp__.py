# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################

{
    'name': 'Sales by Partner Company',
    'version': '8.0.0.1',
    'category': 'Reporting',
    'summary': 'Sales by Partner Company',
    'description': """
##############################################################
          Sales - Partner Company Filter
##############################################################     
    *   This module adds new computed field "Customer Company" which is set to the Company of the Contact if Customer is Contact having parent company; otherwise cutomer itself
    *   Adds Customer Company in Search View > Group by...
    *   Sets Customer Company Group by filter as default on Graph View
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
