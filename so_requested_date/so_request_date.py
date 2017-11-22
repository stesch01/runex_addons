# -*- coding: utf-8 -*-

from openerp import models, fields


class SoRequestedDateSaleOrder(models.Model):
    _inherit = 'sale.order'

    resuested_date_2 = fields.Datetime(related='requested_date')
