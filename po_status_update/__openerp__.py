# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################

{
    'name': 'Purchase Order - Status',
    'version': '8.0.0.1',
    'category': 'Purchasing',
    'summary': 'Purchase Order - Status Update Fix',
    'description': """
##############################################################
          		Purchase Order - Status Update Fix
##############################################################     
	*	This module fixes bug in updating Purchase Order status as Done when all shipment is received and invoiced.
	*	It also fixes missing shipments link related to purchase order.
    """,

    'author': 'Linserv AB',
    'contributors': ['Riyaj Pathan <rjpathan19@gmail.com>'],
    'website': 'www.linserv.se/en/',

    'depends': ['purchase'],
    'data': [
    	'views/purchase.xml',
    ],

    'application': False,
    'auto_install': False,
    'installable': True,
    }
