# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################

from openerp import models, fields, api
from datetime import datetime, timedelta, date as dt

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line')
    def _compute_std_gross_profit(self):
        for order in self:
            gross_profit = 0.0
            for line in order.order_line:
                gross_profit += line.std_gross_profit_line
        
            order.std_gross_profit = gross_profit

    std_gross_profit = fields.Float(compute="_compute_std_gross_profit", string='Standard Gross Profit', store=True)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    std_gross_profit_line = fields.Float('Standard Gross Profit')

    @api.model
    def create(self, vals):
        """Set Gross Profit as Selling price - Cost Price for sold quantity
        """
        if not vals: vals = {}
        if 'purchase_price' in vals and 'price_unit' in vals and 'product_uom_qty' in vals:
            vals['std_gross_profit_line'] = (vals['price_unit'] - vals['purchase_price']) * vals['product_uom_qty']
        return super(SaleOrderLine, self).create(vals)

    @api.multi
    def write(self, vals):
        """Set Gross Profit as Selling price - Cost Price for sold quantity
        """
        if not vals: vals = {}
        for line in self:
            product_id = line.product_id and line.product_id.id
            purchase_price = line.product_id and line.product_id.standard_price or 0.0
            price_unit = line.price_unit
            product_uom_qty = line.product_uom_qty

        if 'price_unit' in vals:
            price_unit = vals['price_unit']
        if 'product_uom_qty' in vals:
            product_uom_qty = vals['product_uom_qty']
        if 'product_id' in vals:
            product_id = vals['product_id']
            purchase_price = self.env['product.product'].browse([product_id])[0].standard_price

        if 'product_id' in vals or 'price_unit' in vals or 'product_uom_qty' in vals:
            vals['std_gross_profit_line'] = (price_unit - purchase_price) * product_uom_qty
        return super(SaleOrderLine, self).write(vals)
    