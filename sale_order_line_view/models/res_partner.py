# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín <esthermartin@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.osv import fields,osv

class ResPartner(osv.osv):
    _inherit = 'res.partner'

    def _sale_order_line_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        # The current user may not have access rights for sale orders
        try:
            for partner in self.browse(cr, uid, ids, context):
                res[partner.id] = len(partner.order_lines)
        except:
            pass
        return res

    _columns = {
        'lines_count': fields.function(_sale_order_line_count, string='Sale Order Lines', type='integer'),
        'order_lines': fields.one2many('sale.order.line','order_partner_id','Sales Order lines')
    }
    