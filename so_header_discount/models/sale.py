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

    so_discount = fields.Float(compute='compute_partner_discount', string='Discount %', readonly=True, Store=True)

    @api.one
    @api.depends('partner_id')
    def compute_partner_discount(self):
    	discount = 0
    	if self.partner_id.parent_id:
    		discount = self.partner_id.parent_id.so_discount or 0.0
    	if not discount:
    		discount = self.partner_id and self.partner_id.so_discount or 0.0
    	self.so_discount = discount