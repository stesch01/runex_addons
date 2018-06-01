# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale


class CartPreview(website_sale):

    @http.route(['/shop/cart/preview'], type='http', auth="public", website=True)
    def quick_preview_cart(self,  **post):
        return request.render("website_sale_cart_preview.cart_preview", {}, headers={'Cache-Control': 'no-cache'})
