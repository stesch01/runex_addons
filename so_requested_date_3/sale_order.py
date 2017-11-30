# -*- coding: utf-8 -*-

from openerp import models, fields


class SoRequestedDateSaleOrder(models.Model):
    _inherit = 'sale.order'

    requested_date = fields.Datetime('Requested Date', readonly=False,
                                      states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=False,
                                      help="Date by which the customer has requested the items to be "
                                           "delivered.\n"
                                           "When this Order gets confirmed, the Delivery Order's "
                                           "expected date will be computed based on this date and the "
                                           "Company's Security Delay.\n"
                                           "Leave this field empty if you want the Delivery Order to be "
                                           "processed as soon as possible. In that case the expected "
                                           "date will be computed using the default method: based on "
                                           "the Product Lead Times and the Company's Security Delay.")