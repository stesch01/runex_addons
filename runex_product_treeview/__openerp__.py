# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    'name': 'Purchase Order - List view',
    'version': '1.0',
    'category': "Tools",
    'summary': 'Purchase Order - List view',
    'description': """
####################################################
            Purchase Order - List view
####################################################
This app modifies tree view of Purchase Orders:
    *   Remove time from Order date column
    *   Remove the Total Column
    *   Add Currency (field: currency.id, model:purchase.order) after Untaxed column 

    """,

    'author': 'Linserv AB',
    'website': 'www.linserv.se',
    'contributors': ['Riyaj Pathan <rjpathan19@gmail.com>',
    ],

    'depends': ['purchase'],
    'data': [
        'views/purchase.xml',
    ],
    
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
