# -*- coding: utf-8 -*-
{
    'name': "so_requested_date",

    'summary': """
        so_requested_date""",

    'description': """
        so_requested_date
    """,

    'author': "UAB Pralo",
    'website': "http://www.pralo.eu",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'sale_order_dates', 'sale_stock'],

    'data': [
        'inherited_sale_stock.xml',
        'inherited_sale_order_dates.xml',
        'inherited_sale_order.xml',
    ],
}