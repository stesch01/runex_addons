# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
#
##############################################################################
{
    'name': 'Runex Add to CartView',
    'version': '1.0',
    'author': 'Linserv AB',
    'category': "Web",
    'website': 'www.linserv.se',
    'description': """Custom runex website views modifications to add quick view of a productTitle wihtout leave shop page and add dropdown view of cart""",
    'depends': ['website', 'website_sale'],
    'data': [
        'views/templates.xml',
        'views/views_updates.xml',
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
