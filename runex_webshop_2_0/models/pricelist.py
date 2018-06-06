# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class Currency(models.Model):
    _inherit = 'res.currency'

    country_ids = fields.One2many(comodel_name='res.country', inverse_name='currency_id', string='Countries')


class res_lang(models.Model):
    _inherit = 'res.lang'

    pricelist = fields.Many2one(
        comodel_name='product.pricelist',
        domain=[('type', '=', 'sale')],
        string='Price List'
    )


class pricelist(models.Model):
    _inherit = 'product.pricelist'

    language_ids = fields.One2many(
        comodel_name='res.lang',
        inverse_name='pricelist',
        string='Languages'
    )


