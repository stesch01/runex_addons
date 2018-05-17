# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################

from openerp import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    so_margin_percent = fields.Float(compute='compute_so_margin_percent', string='Margin %', readonly=True, Store=True, digits=(20,1))

    @api.one
    @api.depends('order_line', 'amount_untaxed')
    def compute_so_margin_percent(self):
        margin = 0
        for sale in self:
            for line in sale.order_line:
                if line.state == 'cancel':
                    continue
                margin += line.margin or 0.0
            if sale.amount_untaxed != 0:
                sale.so_margin_percent = (margin / sale.amount_untaxed) * 100
            else:
                sale.so_margin_percent = 0
            