# -*- coding: utf-8 -*-
{
    'name': "so_ready_to_ship",

    'summary': """
        so_ready_to_ship""",

    'description': """
        so_ready_to_ship
    """,

    'author': "UAB Pralo",
    'website': "http://www.pralo.eu",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'web', 'sale', 'sale_order_line_view'],

    'data': [
        'inherited_sale_order.xml',
        'views/templates.xml',
    ],
}