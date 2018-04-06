# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################

{
    'name': 'Sales Order - Discount',
    'version': '8.0.0.1',
    'category': 'Tools',
    'summary': 'Sales Order - Discount',
    'description': """
##############################################################
          Sales Order - Discount
##############################################################     
This module adds Discount field in Partner (Customer) and Sales Order
    """,

    'author': 'Linserv AB',
    'contributors': ['Riyaj Pathan <rjpathan19@gmail.com>'],
    'website': 'www.linserv.se/en/',

    'depends': ['sale'],
    'data': [ 
        'views/partner.xml',
        'views/sale.xml',
    ],

    'application': False,
    'auto_install': False,
    'installable': True,
    }
