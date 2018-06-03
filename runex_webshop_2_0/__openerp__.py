# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    "name": "RUNEX webshop 2.0",
    "version": "1.0",
    "author": "Linserv AB",
    "category": "Website",
    "summary": "RUNEX webshop 2.0",
    "website": "www.linserv.se",
    "contributors": [
        'Gediminas Venclova <gediminasv@live.com>'
    ],
    "license": "",
    "depends": ['website', 'website_sale'],
    'description': """

        Package of Runex Webshop modifications

    """,
    "demo": [],
    "data": [
        'views/views.xml',
        'views/website_sale_template.xml'
    ],
    "test": [],
    "js": [],
    "css": [],
    "installable": True,
    "auto_install": False,
}
