# -*- coding: utf-8 -*-

from openerp import models, fields

from datetime import datetime


class SoTimestampOnConfirmSaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_button_confirm(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        datetime_now = datetime.now()
        for so in self.browse(cr, uid, ids, context=context):
            so.update({'date_order': datetime_now})
        self.signal_workflow(cr, uid, ids, 'order_confirm')
        if context.get('send_email'):
            self.force_quotation_send(cr, uid, ids, context=context)
        return True