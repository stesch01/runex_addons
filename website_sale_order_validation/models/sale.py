# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[('web_confirmed', 'Web Confirmed')])

    @api.multi
    def action_web_confirm(self):
        for order in self:
            self.write({'state': 'web_confirmed'})

    # Fix the order of states (new stat is added last in view)
    # We want it to be added in the second order.
    @api.model
    def fields_get(self, fields=None, attributes=None):
        fields = super(SaleOrder, self).fields_get(fields, attributes=attributes)
        try:
            if 'state' in fields and 'selection' in fields['state']:
                states = fields['state']['selection']
                draft_index = None
                for pos, state in enumerate(states):
                    if len(state) == 2 and state[0] == 'draft':
                        draft_index = pos
                        break
                if draft_index is not None:
                    web_confirmed_tuple = None
                    for state in states:
                        if len(state) == 2 and state[0] == 'web_confirmed':
                            web_confirmed_tuple = state
                    if web_confirmed_tuple is not None:
                        states.remove(web_confirmed_tuple)
                        states.insert(draft_index+1, web_confirmed_tuple)
        except:
            pass
        try:
            # copy readonly, invisible, required attrs from draft state
            for field_name, field_val in fields.iteritems():
                if 'states' in field_val:
                    for state in field_val['states'].keys():
                        if state == 'draft':
                            field_val['states']['web_confirmed'] = field_val['states'][state][:]
        except:
            pass
        return fields
