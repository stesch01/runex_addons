# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################

{
    'name': 'Sales Order - Margin in Percentage',
    'version': '8.0.0.1',
    'category': 'Tools',
    'summary': 'Sales Order - Margin in Percentage',
    'description': """
##############################################################
          Sales Order - Margin in Percentage
##############################################################     
This module shows Margin in Percentage in Sales Order form
    """,

    'author': 'Linserv AB',
    'contributors': ['Riyaj Pathan <rjpathan19@gmail.com>'],
    'website': 'www.linserv.se/en/',

    'depends': ['sale_margin'],
    'data': [ 
        'views/sale.xml',
    ],

    'application': False,
    'auto_install': False,
    'installable': True,
    }
