# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    'name': "Product Code Replacement",
    "version": "1.0",
    "author": "Linserv AB",
    "category": "Sales Management",
    "summary": "Product Code Replacement",
    "website": "www.linserv.se",
    "contributors": [
        'Gediminas Venclova <gediminasv@live.com>'
    ],
    "license": "",
    'depends': [
        'product'
    ],
    'description': """

        Modification moves product code field from information tab next to product name.

    """,
    "demo": [],
    "data": [
        'views/inherited_product.xml',
    ],
    "test": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    "auto_install": False,

}