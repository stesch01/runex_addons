# -*- coding: utf-8 -*-

from openerp import models, fields


class SoRequestedDateSaleOrder(models.Model):
    _inherit = 'sale.order'

    exworks_date = fields.Date(string='Ex Works Date')
