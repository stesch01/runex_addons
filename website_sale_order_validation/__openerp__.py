# -*- coding: utf-8 -*-

{
    'name': 'eCommerce Order validation',
    'version': '1.0',
    'author': 'Linserv AB',
    'sequence': 1,
    'website': 'www.linserv.se',
    'summary': 'Final Validation for eCommerce order if no payment method exists',
    'contributors': [
        'Azer GHADHOUN <ghadhoun.azer@gmail.com>'
    ],
    'description': """
    Final Validation for eCommerce order if no payment method exists
    """,
    'depends': ['website_sale'],
    'data': [
        'views/sale_workflow.xml',
        'views/sale_views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}

