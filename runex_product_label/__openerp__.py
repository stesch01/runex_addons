# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    'name': 'Runex Product Label',
    'version': '1.0',
    'author': 'Linserv AB',
    'category': "Sales Management",
    'website': 'www.linserv.se',
    'description': """Custom runex product label""",
    'depends': ['stock','report'],
    'data': [
        'reports/report_product_label.xml',
        'reports/report.xml',                   
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
