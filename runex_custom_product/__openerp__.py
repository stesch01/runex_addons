# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    "name": "Runex Custom Product",
    "version": "1.0",
    "author": "Linserv AB",
    "category": "Sales Management",
    "summary": "Runex Custom Product",
    "website": "www.linserv.se",
    "contributors": [
        'Gediminas Venclova <gediminasv@live.com>'
    ],
    "license": "",
    "depends": [
        'base', 'product', 'purchase', 'website_sale'
    ],
    'description': """

        Runex Custom Product

        This module moves "Available On The Website" field to the top of the view, also expands product name field in product view.
    """,
    "demo": [],
    "data": [
        'website_sale.xml',
        'purchase.xml',
        'product.xml',
    ],
    "test": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    "auto_install": False,
}