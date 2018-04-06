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

    so_discount = fields.Float(related="partner_id.so_discount", string='Discount %', readonly=True)

    @api.onchange('partner_id')
    def onchange_partner_for_discount(self):
    	self.so_discount = self.partner_id and self.partner_id.so_discount or 0.0