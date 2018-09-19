# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################

from openerp.osv import osv, fields

class PurchaseOrder(osv.osv):
    _inherit = "purchase.order"

    def _get_picking_ids(self, cr, uid, ids, field_names, args, context=None):
        """Overwrite function to correctly link all shipments related to Purchase Order
        """
        res = {}
        for po_id in ids:
            res[po_id] = []
        query = """
        SELECT picking_id, po.id FROM stock_picking p, stock_move m, purchase_order_line pol, purchase_order po
            WHERE po.id in %s and po.id = pol.order_id and pol.id = m.purchase_line_id and m.picking_id = p.id
            GROUP BY picking_id, po.id
             
        """
        cr.execute(query, (tuple(ids), ))
        picks = cr.fetchall()
        for pick_id, po_id in picks:
            res[po_id].append(pick_id)

            #select picking reference using origin
            po = self.pool.get('purchase.order').browse(cr, uid, [po_id])
            cr.execute("""select id from stock_picking where origin = '%s'"""%(po.name))
            result = cr.fetchall()
            picking_ref = False
            for r in result:
                picking_ref = r[0]
                res[po_id].append(picking_ref)
        return res

    _columns = {
        'picking_ids': fields.function(_get_picking_ids, method=True, type='one2many', relation='stock.picking', string='Picking List', help="This is the list of receipts that have been generated for this purchase order."),
    }

class stock_picking(osv.osv):
    _inherit = "stock.picking"

