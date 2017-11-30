# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    "name": "Sale Order Ready To Ship",
    "version": "1.0",
    "author": "Linserv AB",
    "category": "Sales Management",
    "summary": "Green color order reference name in sales orders views",
    "website": "www.linserv.se",
    "contributors": [
        'Gediminas Venclova <gediminasv@live.com>'
    ],
    "license": "",
    "depends": [
        'base', 'web', 'sale', 'sale_order_line_view', 'sale_order_dates'
    ],
    'description': """
    
        Sale Order Ready To Ship
    
        This module changes color of order reference name in sale order and sale order lines views.
    """,
    "demo": [],
    "data": [
        'inherited_sale_order.xml',
        'views/templates.xml',
    ],
    "test": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    "auto_install": False,
}