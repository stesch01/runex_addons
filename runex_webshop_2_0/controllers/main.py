# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
import werkzeug
from openerp.addons.website.models.website import slug
from openerp.addons.website_sale.controllers.main import website_sale, QueryURL
PPG = 52 # Products Per Page
PPR = 4  # Products Per Row
import logging
_logger = logging.getLogger(__name__)

class table_compute(object):
    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx+x>=PPR:
                    res = False
                    break
                row = self.table.setdefault(posy+y, {})
                if row.setdefault(posx+x) is not None:
                    res = False
                    break
            for x in range(PPR):
                self.table[posy+y].setdefault(x, None)
        return res

    def process(self, products, ppg):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        for p in products:
            x = min(max(p.website_size_x, 1), PPR)
            y = min(max(p.website_size_y, 1), PPR)
            if index>=ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(pos%PPR, pos/PPR, x, y):
                pos += 1
            # if 21st products (index 20) and the last line is full (PPR products in it), break
            # (pos + 1.0) / PPR is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= ppg and ((pos + 1.0) / PPR) > maxy:
                break

            if x==1 and y==1:   # simple heuristic for CPU optimization
                minpos = pos/PPR

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos/PPR)+y2][(pos%PPR)+x2] = False
            self.table[pos/PPR][pos%PPR] = {
                'product': p, 'x':x, 'y': y,
                'class': " ".join(map(lambda x: x.html_class or '', p.website_style_ids))
            }
            if index<=ppg:
                maxy=max(maxy,y+(pos/PPR))
            index += 1

        # Format table according to HTML needs
        rows = self.table.items()
        rows.sort()
        rows = map(lambda x: x[1], rows)
        for col in range(len(rows)):
            cols = rows[col].items()
            cols.sort()
            x += len(cols)
            rows[col] = [c for c in map(lambda x: x[1], cols) if c != False]

        return rows


class website_sales(website_sale):

    def get_pricelist(self):
        return request.env.user.sudo().partner_id.property_product_pricelist

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
        '/shop/tag/<model("product.tags"):tag_id>',
        '/shop/tag/<model("product.tags"):tag_id>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=1, tag_id=None, category=None, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        if tag_id:
            category = None
        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attrib_set = set([v[1] for v in attrib_values])
        if not tag_id:
            domain = self._get_search_domain(search, category, attrib_values)
        else:
            domain = self._get_search_domain_tags(search, tag_id, attrib_values)

        tag = tag_id and int(tag_id)
        if tag:
            keep = QueryURL('/shop/tag/%s/' % tag, search=search, attrib=attrib_list)
        else:
            keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list)

        if not context.get('pricelist'):
            pricelist = self.get_pricelist()
            context['pricelist'] = int(pricelist)
        else:
            pricelist = pool.get('product.pricelist').browse(cr, uid, context['pricelist'], context)

        product_obj = pool.get('product.template')

        url = "/shop"
        product_count = product_obj.search_count(cr, uid, domain, context=context)
        if search:
            post["search"] = search
        if tag_id:
            tag = pool['product.tags'].browse(cr, uid, int(tag_id), context=context)
            url = "/shop/tag/%s" % slug(tag)
        if category:
            category = pool['product.public.category'].browse(cr, uid, int(category), context=context)
            url = "/shop/category/%s" % slug(category)

        if attrib_list:
            post['attrib'] = attrib_list

        ppg = PPG
        if post.get('limit'):
            limit = post.get('limit')
            try:
                int(limit)
                ppg = abs(int(limit))
            except:
                pass
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        post['order'] = post.get('order', 'name')
        product_ids = product_obj.search(cr, uid, domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post), context=context)
        products = product_obj.browse(cr, uid, product_ids, context=context)

        style_obj = pool['product.style']
        style_ids = style_obj.search(cr, uid, [], context=context)
        styles = style_obj.browse(cr, uid, style_ids, context=context)

        category_obj = pool['product.public.category']
        category_ids = category_obj.search(cr, uid, [('parent_id', '=', False)], context=context)
        categs = category_obj.browse(cr, uid, category_ids, context=context)

        attributes_obj = request.registry['product.attribute']
        attributes_ids = attributes_obj.search(cr, uid, [], context=context)
        attributes = attributes_obj.browse(cr, uid, attributes_ids, context=context)

        from_currency = pool.get('product.price.type')._get_field_currency(cr, uid, 'list_price', context)
        to_currency = pricelist.currency_id
        compute_currency = lambda price: pool['res.currency']._compute(cr, uid, from_currency, to_currency, price, context=context)
        view_type = 'grid_view'
        if post.get('view_type') and post.get('view_type') == 'list_view':
            view_type = 'list_view'

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'page': page,
            'pager': pager,
            'pricelist': pricelist,
            'products': products,
            'bins': table_compute().process(products, ppg),
            'rows': PPR,
            'styles': styles,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'style_in_product': lambda style, product: style.id in [s.id for s in product.website_style_ids],
            'attrib_encode': lambda attribs: werkzeug.url_encode([('attrib',i) for i in attribs]),
            'product_count': product_count,
            'view_type': view_type,
            'limit': ppg,
            'url': url,
        }
        return request.website.render("website_sale.products", values)


    # @http.route([
    #     '/shop',
    #     '/shop/page/<int:page>',
    #     '/shop/category/<model("product.public.category"):category>',
    #     '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    # ], type='http', auth="public", website=True)
    # def shop(self, page=0, category=None, search='', **post):
    #     ppg = PPG
    #     res = super(website_sale, self).shop(page=page,
    #                                         category=category,
    #                                         search=search, ppg=ppg,
    #                                         **post)
    #     cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
    #     if post.get('limit'):
    #         limit = post.get('limit')
    #         try:
    #             int(limit)
    #             ppg = abs(int(limit))
    #         except:
    #             pass
    #     if not context.get('pricelist'):
    #         pricelist = self.get_pricelist()
    #         context['pricelist'] = int(pricelist)
    #     else:
    #         pricelist = pool.get('product.pricelist').browse(cr, uid, context['pricelist'], context)
    #     post['order'] = post.get('order', 'name')
    #     view_type = 'grid_view'
    #     if post.get('view_type') and post.get('view_type') == 'list_view':
    #         view_type = 'list_view'
    #
    #     attrib_list = request.httprequest.args.getlist('attrib')
    #     attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
    #     domain = self._get_search_domain(search, category, attrib_values)
    #     product_obj = pool.get('product.template')
    #     product_count = product_obj.search_count(cr, uid, domain, context=context)
    #
    #     res.qcontext.update({
    #         'page': page,
    #         'bins': table_compute().process(res.qcontext.get('products'), ppg),
    #         'product_count': product_count,
    #         'view_type': view_type,
    #         'limit': ppg,
    #         # 'url': url,
    #         'url': res.qcontext.get('keep'),
    #     })
    #     return res

    def _get_search_domain(self, search, category, attrib_values):
        domain = request.website.sale_product_domain()

        if search:
            search_fields = request.env['ir.config_parameter'].get_param('alt.products.search.fields', 'name description description_sale product_variant_ids.default_code').split(" ")
            for srch in search.split(" "):
                domain += ['|' for x in range(len(search_fields) - 1)] + [(f, 'ilike', srch) for f in search_fields]
        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]

        return domain

    def _get_search_domain_tags(self, search, tag, attrib_values):
        domain = request.website.sale_product_domain()

        if search:
            search_fields = request.env['ir.config_parameter'].get_param('alt.products.search.fields', 'name description description_sale product_variant_ids.default_code').split(" ")
            for srch in search.split(" "):
                domain += ['|' for x in range(len(search_fields) - 1)] + [(f, 'ilike', srch) for f in search_fields]
        if tag:
            domain += [('tag_ids', 'in', [int(tag)])]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]
        return domain

