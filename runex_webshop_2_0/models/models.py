# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import fields as osv_fields
from openerp.osv import osv
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _property_product_pricelist(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            # if id == self.pool.get('ir.model.data').get_object_reference(cr, uid, 'base', 'public_partner')[1]:
            if True:
                lang = request.context.get('lang')
                pricelist = self.pool.get('product.pricelist').browse(cr, uid,
                    self.pool.get('product.pricelist').search(cr, uid,
                        [('language_ids.code', '=', lang)], context=context), context=context)
                if not pricelist:
                    # Fallback if no pricelist found
                    company_list = self.pool.get('website').search(cr, uid, [], limit=1)
                    company = self.pool.get('website').browse(cr, uid, company_list).company_id
                    langs = lang.split('_')
                    country_code = langs and len(langs) == 2 and langs[1]
                    companies = (False,) if not company else (False, company.id)
                    if country_code:
                        domain = []
                        # force using euro if country is GB
                        if country_code == 'GB':
                            domain += [('currency_id.name', '=', 'EUR')]
                        else:
                            domain += [('currency_id.country_ids.code', '=', country_code)]
                        domain += [
                            ('company_id', 'in', companies),
                            ('type', '=', 'sale'),
                            ('version_id', '!=', False),
                        ]
                        pricelist_list = self.pool.get('product.pricelist').search(
                            cr,uid,domain, context=context,limit=1
                        )
                        if pricelist_list:
                            pricelist = self.pool.get('product.pricelist').browse(cr, uid,pricelist_list ,context=context)
                    if not pricelist:
                        raise Warning(_("No pricelist found for your language! Please contact the administrator."))
            # else:
            #     partner = self.pool.get('res.partner').read(cr, uid, id, ['partner_product_pricelist', 'lang', 'commercial_partner_id'], context=context)
            #     # The compute breaks the commercial fields handling. Check if this partner is it's own commercial partner to account for that.
            #     if partner['commercial_partner_id'] and partner['commercial_partner_id'][0] != id:
            #         # Get the pricelist from the commercial partner and move along.
            #         res[id] = self._property_product_pricelist(cr, uid, [partner['commercial_partner_id'][0]], name, arg, context)[partner['commercial_partner_id'][0]]
            #         continue
            #     lang = partner['lang']
            #     pricelist = self.pool.get('product.pricelist').browse(cr, uid,
            #         partner['partner_product_pricelist'] and partner['partner_product_pricelist'][0] or [], context=context)
            if pricelist:
                res[id] = pricelist.id
            else:
                res[id] = False
        return res

    _columns = {
        'property_product_pricelist': osv_fields.function(
            _property_product_pricelist,
            type='many2one',
            relation='product.pricelist',
            domain=[('type', '=', 'sale')],
            string="Sale Pricelist",
            help="This pricelist will be used, instead of the default one, for sales to the current partner"),
    }


class Currency(models.Model):
    _inherit = 'res.currency'

    country_ids = fields.One2many(comodel_name='res.country', inverse_name='currency_id', string='Countries')


class Lang(models.Model):
    _inherit = 'res.lang'

    pricelist = fields.Many2one(
        comodel_name='product.pricelist',
        domain=[('type', '=', 'sale')],
        string='Price List'
    )


class Pricelist(models.Model):
    _inherit = 'product.pricelist'

    language_ids = fields.One2many(
        comodel_name='res.lang',
        inverse_name='pricelist',
        string='Languages'
    )


class ProductCategory(models.Model):
    _inherit = 'product.public.category'

    description = fields.Text(string='Description')
