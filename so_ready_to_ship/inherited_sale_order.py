# -*- coding: utf-8 -*-

from openerp import models, fields


class SoReadyToShipSaleOrder(models.Model):
    _inherit = 'sale.order'

    have_qty = fields.Boolean(string='Have Enough Quantity', compute='_compute_have_qty')

    def _compute_have_qty(self):
        for so in self:
            if all(so_line.qty_on_hand >= so_line.product_uom_qty for so_line in so.order_line):
                so.have_qty = True
            else:
                so.have_qty = False


class SoReadyToShipSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_on_hand = fields.Float(related='product_id.product_tmpl_id.qty_available', string="On Hand")