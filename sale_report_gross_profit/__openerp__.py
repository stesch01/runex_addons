# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################

{
    'name': 'Sales Report - Gross Profit',
    'version': '8.0.0.1',
    'category': 'Reporting',
    'summary': 'Sales Report - Gross Profit',
    'description': """
##############################################################
          Sales Report - Gross Profit
##############################################################     
This module adds computed field "Standard Gross Profit" in Sales Order computed as actual sale price - standard price at the time of sale for sold quantity
    """,

    'author': 'Linserv AB',
    'contributors': ['Riyaj Pathan <rjpathan19@gmail.com>'],
    'website': 'www.linserv.se/en/',

    'depends': ['sale'],
    'data': [ 
    ],

    'application': False,
    'auto_install': False,
    'installable': True,
    }
