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

    def cron_compute_po_status(self, cr, uid, ids=None):
        """Function which checks all Approved Purchase orders and checks if PO status can be marked as Done
        """ 
        orders = self.pool.get('purchase.order').search(cr, uid, [('state','=','approved')])
        for order in self.pool.get('purchase.order').browse(cr, uid, orders):
            self.compute_po_status(cr, uid, [order.id])
        return True

    def compute_po_status(self, cr, uid, ids, context=None):
        """This function updates PO status as Done if 
        - related shipment is received AND
        - PO is fully invoiced
        """
        for po in self.browse(cr, uid, ids):
            po_products_data = {}
            for line in po.order_line:
                if line.product_id and line.product_id.id not in po_products_data:
                    po_products_data[line.product_id.id] = 0
            for line in po.order_line:
                if line.product_id:
                    po_products_data[line.product_id.id] += line.product_qty
            
            #get processed shipments:
            picking_products_data = {}
            for picking in po.picking_ids:
                if picking.state == 'done':
                    for move in picking.move_lines:
                        if move.product_id and move.product_id.id not in picking_products_data:
                            picking_products_data[move.product_id.id] = 0
            for picking in po.picking_ids:
                if picking.state == 'done':
                    for move in picking.move_lines:
                        if move.product_id:
                            picking_products_data[move.product_id.id] += move.product_uom_qty

            # compare po products & received products:
            flag = False
            for prod in po_products_data:
                if prod in picking_products_data.keys():
                    if picking_products_data[prod] >= po_products_data[prod]:
                        flag = True
                    else:
                        flag = False
                        break
                else:
                    flag = False
                    break

            #check if PO is invoiced
            invoice_total, invoice_flag = 0, False
            for invoice in po.invoice_ids:
                if invoice.state not in ('draft', 'proforma', 'proforma2'):
                    invoice_total += invoice.amount_total
            if invoice_total >= po.amount_total:
                invoice_flag = True

            if flag and invoice_flag:
                self.write(cr, uid, ids, {'state': 'done'})
            return True

class stock_picking(osv.osv):
    _inherit = "stock.picking"

    def write(self, cr, uid, ids, vals, context=None):
        res = super(stock_picking, self).write(cr, uid, ids, vals, context)
        if ('state' in vals and vals['state'] == 'done') or 'date_done' in vals:
            for rec in self.browse(cr, uid, ids):
                po = self.pool.get('purchase.order').search(cr, uid, [('name','=',rec.origin)], limit=1)
                if po:
                    self.pool.get('purchase.order').compute_po_status(cr, uid, po)
        return res

class AccountInvoice(osv.osv):
    _inherit = "account.invoice"

    def write(self, cr, uid, ids, vals, context=None):
        """Check & update related PO Status
        """
        res = super(AccountInvoice, self).write(cr, uid, ids, vals, context)
        if 'state' in vals and vals['state'] == 'open':
            for rec in self.browse(cr, uid, ids):
                if rec.type == 'in_invoice':
                    po = self.pool.get('purchase.order').search(cr, uid, [('name','=',rec.origin)], limit=1)
                    if po:
                        self.pool.get('purchase.order').compute_po_status(cr, uid, po)
                    else:
                        picking = self.pool.get('stock.picking').search(cr, uid, [('name','=',rec.origin)], limit=1)
                        if picking:
                            picking_origin = self.pool.get('stock.picking').browse(cr, uid, picking)[0].origin
                            po = self.pool.get('purchase.order').search(cr, uid, [('name','=',picking_origin)], limit=1)
                            if po:
                                self.pool.get('purchase.order').compute_po_status(cr, uid, po)
        return res
