# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
#
##############################################################################
{
    'name': 'Runex App Modifications v3.0',
    'version': '1.0',
    'author': 'Linserv AB',
    'category': "Web",
    'website': 'www.linserv.se',
    'description': """Custom runex website views modifications""",
    'depends': ['website', 'website_sale', 'website_sale_suggest_create_account'],
    'data': [
        'views/templates.xml',
        'views/views_updates.xml',
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
