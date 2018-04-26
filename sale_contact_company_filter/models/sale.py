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

    @api.depends('partner_id')
    def _set_partner_company(self):
        for order in self:
            partner_company_id = order.partner_id.id
            if not order.partner_id.is_company and order.partner_id.parent_id:
                partner_company_id = order.partner_id.parent_id.id

            order.partner_company_id = partner_company_id

    partner_company_id = fields.Many2one('res.partner', compute="_set_partner_company", string='Customer Company', store=True)
