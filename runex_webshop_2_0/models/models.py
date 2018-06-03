# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import fields as osv_fields
from openerp.osv import osv
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    def _property_product_pricelist(self):

        for partner in self:
            lang = request.context.get('lang')
            pricelist = self.env['res.lang'].search(
                    [('code', '=', lang)], limit=1
            ).pricelist
            if not pricelist:
                # Fallback if no pricelist found
                company = self.env['website'].search([], limit=1).company_id
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
                    pricelist = self.env['product.pricelist'].search(
                        domain, limit=1
                    )
                if not pricelist:
                    raise Warning(_("No pricelist found for your language! Please contact the administrator."))
            if pricelist:
                partner.property_product_pricelist = pricelist

    property_product_pricelist = fields.Many2one(
        compute='_property_product_pricelist',
        relation='product.pricelist',
        string="Sale Pricelist",
        help="This pricelist will be used, instead of the default one, for sales to the current partner"
    )


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
