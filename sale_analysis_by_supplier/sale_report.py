# -*- coding: utf-8 -*-

from openerp import models, fields, _


class SaleAnalysisBySUpplierSaleReport(models.Model):
    _inherit = "sale.report"

    seller_id = fields.Many2one('res.partner', string='Main Supplier', help="Main Supplier who has highest priority in Supplier List.", readonly=True)

    def _select(self):
        return super(SaleAnalysisBySUpplierSaleReport, self)._select() + ", l.seller_id as seller_id"

    def _group_by(self):
        return super(SaleAnalysisBySUpplierSaleReport, self)._group_by() + ", l.seller_id"
