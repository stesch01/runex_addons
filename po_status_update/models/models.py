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

    def _progress_invoice_check(self, cr, uid, ids, name, args, context=None):
        res = {}
        for po in self.browse(cr,uid,ids):
            state = 'ni'
            pickings = []
            pickings += [picking.id for picking in po.picking_ids]
            if po.invoice_method == 'picking':#invoices from Incoming Shipment
                if len(pickings) == 1:
                    for pick in self.pool.get('stock.picking').browse(cr, uid, pickings):
                        invoice = self.pool.get('account.invoice').search(cr, uid, [('origin','=',pick.name)])
                        state = 'ni'
                        if invoice:
                            inv_state = self.pool.get('account.invoice').browse(cr, uid, invoice)[0].state
                            state = 'fp'
                            if inv_state in ('open','proforma'):
                                state = 'fi'
                            elif inv_state == 'draft':
                                state = 'draft'
                            elif inv_state == 'cancel':
                                state = 'cancel' 
                elif pickings: #more than one pickings:
                    inv_count, inv_total = 0, 0.0
                    for pick in self.pool.get('stock.picking').browse(cr, uid, pickings):
                        invoice = self.pool.get('account.invoice').search(cr, uid, [('origin','=',pick.name)])
                        invoice_check, inv_flag, draft_flag = False, False, False
                        if invoice:
                            invoice_check = True
                            inv_state = self.pool.get('account.invoice').browse(cr, uid, invoice)[0].state
                            inv_total += self.pool.get('account.invoice').browse(cr, uid, invoice)[0].amount_total
                            if inv_state == 'paid':
                                inv_count = inv_count + 1
                            elif inv_state in ('open', 'proforma'):
                                inv_flag = True
                            elif inv_state == 'draft':
                                draft_flag = True
                    state = 'ni'
                    if inv_count == len(pickings):
                        state = 'fp'
                    elif inv_count != 0:
                        # check for po & invoice amount
                        if po.amount_total <= inv_total:
                            state = 'fp'
                        else:
                            state = 'pp'
                    elif inv_flag and draft_flag:
                        state = 'fi'
                    elif not inv_flag and draft_flag:
                        state = 'draft'
                    elif invoice_check:
                        state = 'cancel'
            if not pickings or po.invoice_method != 'picking':#invoices from PO
                invoices = []
                invoices += [invoice.id for invoice in po.invoice_ids]
                if len(invoices) == 1:
                    inv_state = self.pool.get('account.invoice').browse(cr, uid, invoices)[0].state
                    state = 'fp'
                    if inv_state in ('open','proforma'):
                        state = 'fi'
                    elif inv_state == 'draft':
                        state = 'draft'
                    elif inv_state == 'cancel':
                        state = 'cancel' 
                elif invoices: #more than one invoices:
                    inv_count = 0
                    invoice_check, inv_flag, draft_flag = False, False, False
                    for invoice in self.pool.get('account.invoice').browse(cr, uid, invoices):
                        inv_state = invoice.state
                        if inv_state == 'paid':
                            inv_count = inv_count + 1
                        elif inv_state in ('open', 'proforma'):
                            inv_flag = True
                        elif inv_state == 'draft':
                            draft_flag = True
                    state = 'ni'
                    if inv_count == len(invoices):
                        state = 'fp'
                    elif inv_count != 0:
                        state = 'pp'
                    elif inv_flag and draft_flag:
                        state = 'fi'
                    elif not inv_flag and draft_flag:
                        state = 'draft'
                    elif invoice_check:
                        state = 'cancel'
            res[po.id] = state
        return res

    def _progress_check(self, cr, uid, ids, name, args, context=None):
        res = {}
        for po in self.browse(cr,uid,ids):
            state = 'na'
            pickings = []
            pickings += [picking.id for picking in po.picking_ids]
            if len(pickings) == 1:
                for pick in self.pool.get('stock.picking').browse(cr, uid, pickings):
                    if pick.in_state == 'confirmed':
                        state = 'wa'
                    elif pick.in_state in ('draft', 'partially_available', 'assigned'):
                        state = 'rp'
                    elif pick.in_state == 'cancel':
                        state = 'cn'
                    elif pick.in_state == 'done':
                        state = 'pi'
            elif pickings: #more than one pickings:
                pick_count = 0
                for pick in self.pool.get('stock.picking').browse(cr, uid, pickings):
                    pick_cancel = False
                    if pick.in_state == 'done':
                        pick_count = pick_count + 1
                    if pick.in_state == 'cancelled':
                        pick_cancel = True
                if pick_count == len(pickings):
                    state = 'pi'
                elif pick_count != 0:
                    state = 'pp'
                elif pick_cancel:
                    state = 'rp'
            res[po.id] = state
        return res

    _columns = {
        'picking_ids': fields.function(_get_picking_ids, method=True, type='one2many', relation='stock.picking', string='Picking List', help="This is the list of receipts that have been generated for this purchase order."),
        'invoice_state': fields.function(_progress_invoice_check, selection=[
                                ('na','Not Applicable'),
                                ('ni','Not Invoiced'),
                                ('draft', 'Draft Invoice'),
                                ('cancel', 'Cancelled'),
                                ('pi','Partially Invoiced'),
                                ('pp','Partially Paid'),
                                ('fi','Invoiced'),
                                ('fp','Paid')], type='selection', string='Invoice State'),
        'receive_state': fields.function(_progress_check, selection=[
                                ('na','Not Applicable'),
                                ('wa','Waiting Availability'),
                                ('rp','Ready to Receive'),
                                ('pp','Partially Received'),
                                ('pi','Received'),
                                ('cn','Cancelled')], type='selection', string='Receive State'),
    }

class stock_picking(osv.osv):
    _inherit = "stock.picking"

    _columns = {
        'in_state': fields.related('state', type='selection', selection=[
                ('draft', 'Draft'),
                ('cancel', 'Cancelled'),
                ('waiting', 'Waiting Another Operation'),
                ('confirmed', 'Waiting Availability'),
                ('partially_available', 'Partially Available'),
                ('assigned', 'Ready to Receive'),
                ('done', 'Received'),
                ], string='Status', store=False),
    }
