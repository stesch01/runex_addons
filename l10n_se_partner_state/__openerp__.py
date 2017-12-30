# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    'name': 'Partner - State Visible',
    'version': '1.0',
    'category': "Tools",
    'summary': 'Partner - State Visible',
    'description': """
####################################################
            Partner - State Visible
####################################################
This app removes modifier defined in l10n_se app which makes State field invisible.
    """,

    'author': 'Linserv AB',
    'website': 'www.linserv.se',
    'contributors': ['Riyaj Pathan <rjpathan19@gmail.com>',
    ],

    'depends': ['l10n_se'],
    'data': [
        'views/partner.xml',
    ],
    
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
