# -*- coding: utf-8 -*-


from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale


class WesbiteOrderValidation(website_sale):

    @http.route(['/shop/order/validate'], type='http', auth="public", website=True)
    def validate_order(self, **post):
        cr, uid, context = request.cr, request.uid, request.context
        order = request.website.sale_get_order(context=context)
        if order:
            request.website.sale_reset(context=context)
            if order.state == 'draft':
                order.sudo().write({'state': 'web_confirmed'})
            return request.redirect('/shop/confirmation')
        return request.redirect('/shop')
