# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    "name": "Sale Order Request Date",
    "version": "3.0",
    "author": "Linserv AB",
    "category": "Sales Management",
    "summary": "Sale Order Requested Date Field Repositioning",
    "website": "www.linserv.se",
    "contributors": [
        'Gediminas Venclova <gediminasv@live.com>'
    ],
    "license": "",
    "depends": [
        'base', 'sale_order_dates', 'sale_stock'
    ],
    'description': """

        Sale Order Requested Date Field Repositioning

        This module repositions field requested date in sale order, also adds custom permissions. Removes Warehouse field.
    """,
    "demo": [],
    "data": [
        'inherited_sale_stock.xml',
        'inherited_sale_order_dates.xml',
        'inherited_sale_order.xml',
    ],
    "test": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    "auto_install": False,
}