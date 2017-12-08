# -*- coding: utf-8 -*-

from openerp import models, fields, _


class SaleAnalysisBySUpplierSale(models.Model):
    _inherit = 'sale.order.line'

    seller_id = fields.Many2one(related='product_id.product_tmpl_id.seller_id', store=True)
