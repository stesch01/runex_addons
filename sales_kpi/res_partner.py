# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2017 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _
from datetime import datetime, timedelta
import json

import logging
_logger = logging.getLogger(__name__)

from openerp.osv import fields as ofields, osv

class ResPartner(osv.osv):
    _inherit = 'res.partner'

    def _kpi_sales(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        # The current user may not have access rights for sale orders
        try:
            for partner in self.browse(cr, uid, ids, context):
                y1 = self.pool.get('account.fiscalyear').browse(self.pool.get('account.fiscalyear').finds(cr, uid, dt=fields.Date.today(), exception=False))
                y2 = self.pool.get('account.fiscalyear').browse(self.pool.get('account.fiscalyear').finds(cr, uid, dt=fields.Date.to_string(datetime(year=datetime.today().year-1,month=datetime.today().month,day=datetime.today().day)), exception=False))
                y3 = self.pool.get('account.fiscalyear').browse(self.pool.get('account.fiscalyear').finds(cr, uid, dt=fields.Date.to_string(datetime(year=datetime.today().year-2,month=datetime.today().month,day=datetime.today().day)), exception=False))
                #~ days = (datetime.today() - datetime(datetime.today().year,1,1)).days / 365.0   # Make all years comparable
                #~ raise Warning(days)
                kpi_sales =  json.dumps([
                    {'value': sum(partner.sale_order_ids.filtered(lambda o: o.date_order >= y1.date_start ).mapped('amount_untaxed')) if y1 else 0.0,
                        'tooltip':y1.code if y1 else ''},
                    {'value': sum(partner.sale_order_ids.filtered(lambda o: o.date_order >= y2.date_start and o.date_order < y2.date_stop ).mapped('amount_untaxed')) if y2 else 0.0,
                        'tooltip':y2.code if y2 else ''},
                    {'value': sum(partner.sale_order_ids.filtered(lambda o: o.date_order >= y3.date_start and o.date_order < y3.date_stop ).mapped('amount_untaxed')) if y3 else 0.0,
                        'tooltip':y3.code if y3 else ''}])

                res[partner.id] = kpi_sales
        except:
            pass
        return res

    _columns = {
        'kpi_sales': ofields.function(_kpi_sales, string='KPI Sales', type='char', store=True),
    }
    

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    @api.depends('order_id.date_order')
    def _kpi_year(self):
        self.kpi_year = self.env['account.fiscalyear'].browse(self.env['account.fiscalyear'].finds(exception=False,dt=self.order_id.date_order)).code
    kpi_year = fields.Char(compute='_kpi_year',store=True)

    #date_order
    #date_order
