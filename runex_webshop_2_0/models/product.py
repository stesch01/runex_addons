# coding=utf-8
from openerp import models, fields, api, _, exceptions, SUPERUSER_ID
from openerp.addons.website.models.website import slug


class Product(models.Model):
    _inherit = "product.template"

    tag_ids = fields.Many2many(
        comodel_name='product.tags',
        column1='product_id',
        column2='tag_id',
        relation='product_tags_rel',
        string='Tags'
    )


class ProductTag(models.Model):
    _name = "product.tags"

    @api.multi
    def _get_url(self):
        for tag in self:
            tag.url = "/shop/tag/%s" % slug(tag)

    name = fields.Char(size=128, string="Name", required=True)
    url = fields.Char(
        compute='_get_url',
        string="Website Url",
    )
    product_ids = fields.Many2many(
        comodel_name='product.template',
        column1='tag_id',
        column2='product_id',
        relation='product_tags_rel',
        string='Products'
    )

