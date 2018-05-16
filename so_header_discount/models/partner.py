# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp

class ResPartner(models.Model):
    _inherit = "res.partner"

    so_discount = fields.Float('Discount %', digits_compute=dp.get_precision('Account'))
    
    @api.onchange('is_company', 'parent_id')
    def onchange_is_company(self):
        for partner in self:
            if not partner.is_company:
                partner.so_discount = partner.parent_id and partner.parent_id.so_discount or 0


    @api.model
    def create(self, vals):
        if not vals: vals = {}
        if 'is_company' in vals:
            if vals['is_company'] is False:
                if vals['parent_id']:
                    company_discount = self.browse([vals['parent_id']]).so_discount
                    vals['so_discount'] = company_discount
        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        if not vals: vals = {}
        for partner in self:
            if 'is_company' in vals or 'parent_id' in vals or 'so_discount' in vals:
                is_company, parent = False, False
                if 'is_company' in vals:
                    is_company = vals['is_company']
                else:
                    is_company = partner.is_company

                if is_company is False:
                    if 'parent_id' in vals:
                        parent = vals['parent_id']
                    else:
                        parent = partner.parent_id.id

                    company_discount = self.browse([parent]).so_discount
                    vals['so_discount'] = company_discount
                
                else:#if its company, update SO discount in all its Contacts
                    company_discount = partner.so_discount
                    if 'so_discount' in vals:
                        company_discount = vals['so_discount']

                    contact_ids = self.search([('parent_id','=',partner.id), ('is_company','=',False)])
                    contacts = []
                    temp = [contacts.append(str(c.id)) for c in contact_ids]
                    contact_result = ', '.join(contacts)
                    if contacts:
                        partner._cr.execute("""update res_partner set so_discount = %s where id in (%s);"""%(company_discount, contact_result))

            return super(ResPartner, partner).write(vals)
