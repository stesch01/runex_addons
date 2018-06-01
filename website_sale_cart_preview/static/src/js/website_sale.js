$(document).ready(function () {
$('.oe_website_sale').each(function () {
    var oe_website_sale = this;

    $('body').on('click', '#modal_optional_products .js_goto_shop', function(){
        $('#preview_content').attr('data-changed', "1");
    });
    var shopping_cart_link = $('#add_to_cart_preview > a');
    var shopping_cart_link_counter;
    shopping_cart_link.on("mouseenter",function () {
        var self = this;
        clearTimeout(shopping_cart_link_counter);
        $content = $('#add_to_cart_preview').find('.dropdown-content');
        $content.hide();
        $content.on("mouseleave", function () {
            $(self).trigger('mouseleave');
        });
        shopping_cart_link_counter = setTimeout(function(){
            if ($('#preview_content').attr('data-changed') != "1"){
                $content.show();
                return;
            }
            if($(self).is(':hover') && !$content.is(":visible"))
            {
                $.get("/shop/cart/preview")
                    .then(function (data) {
                        $('#preview_content').replaceWith($(data));
                        $content = $('#add_to_cart_preview').find('.dropdown-content');
                        $content.show();
                        $content.on("mouseleave", function () {
                            $(self).trigger('mouseleave');
                        });
                    });
            }
        }, 100);
    }).on("mouseleave", function () {
        setTimeout(function () {
            $content_hover = $('#add_to_cart_preview').find('.dropdown-content:hover');
            $link_hover = $('#add_to_cart_preview:hover');
            if(!$content_hover.length && !$link_hover.length) {
                $('#add_to_cart_preview .dropdown-content').hide();
            }
        }, 100);
    });

    function price_to_str(price) {
        var l10n = openerp._t.database.parameters;
        var precision = 2;
        if ($(".decimal_precision").length) {
            var dec_precision = $(".decimal_precision").first().data('precision');
            //Math.log10 is not implemented in phantomJS
            dec_precision = Math.round(Math.log(1/parseFloat(dec_precision))/Math.log(10));
            if (!isNaN(dec_precision)) {
                precision = dec_precision;
            }
        }
        var formatted = _.str.sprintf('%.' + precision + 'f', price).split('.');
        formatted[0] = insert_thousand_seps(formatted[0]);
        return formatted.join(l10n.decimal_point);
    }
    function insert_thousand_seps(num) {
        var l10n = openerp._t.database.parameters;
        var negative = num[0] === '-';
        num = (negative ? num.slice(1) : num);
        // retro-compatibilit: if no website_id and so l10n.grouping = []
        var grouping = l10n.grouping instanceof Array ? l10n.grouping : JSON.parse(l10n.grouping);
        return (negative ? '-' : '') + intersperse(
            num, grouping, l10n.thousands_sep);
    }
    function intersperse(str, indices, separator) {
        separator = separator || '';
        var result = [], last = str.length;

        for(var i=0; i<indices.length; ++i) {
            var section = indices[i];
            if (section === -1 || last <= 0) { break; }
            else if(section === 0 && i === 0) { break; }
            else if (section === 0) { section = indices[--i]; }
            result.push(str.substring(last-section, last));
            last -= section;
        }
        var s = str.substring(0, last);
        if (s) { result.push(s); }
        return result.reverse().join(separator);
    }

    // on input cart change: events are not fired for cart preview input change
    $(oe_website_sale).find(".oe_cart input.js_quantity").off("change");
    $(oe_website_sale).on("change", ".oe_cart input.js_quantity", function () {
        var $input = $(this);
        if ($input.data('update_change')) {
            return;
        }
        var value = parseInt($input.val(), 10);
        var $dom = $(this).closest('tr');
        var default_price = parseFloat($dom.find('.text-danger > span.oe_currency_value').text());
        var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
        var line_id = parseInt($input.data('line-id'),10);
        var product_id = parseInt($input.data('product-id'),10);
        var product_ids = [product_id];
        $dom_optional.each(function(){
            product_ids.push($(this).find('span[data-product-id]').data('product-id'));
        });
        if (isNaN(value)) value = 0;
        $input.data('update_change', true);
        openerp.jsonRpc("/shop/get_unit_price", 'call', {
            'product_ids': product_ids,
            'add_qty': value,
            'use_order_pricelist': true,
            'line_id': line_id})
        .then(function (res) {
            //basic case
            $dom.find('span.oe_currency_value').last().text(price_to_str(res[product_id]));
            $dom.find('.text-danger').toggle(res[product_id]<default_price && (default_price-res[product_id] > default_price/100));
            //optional case
            $dom_optional.each(function(){
                var id = $(this).find('span[data-product-id]').data('product-id');
                var price = parseFloat($(this).find(".text-danger > span.oe_currency_value").text());
                $(this).find("span.oe_currency_value").last().text(price_to_str(res[id]));
                $(this).find('.text-danger').toggle(res[id]<price && (price-res[id]>price/100));
            });
            openerp.jsonRpc("/shop/cart/update_json", 'call', {
            'line_id': line_id,
            'product_id': parseInt($input.data('product-id'),10),
            'set_qty': value})
            .then(function (data) {
                $input.data('update_change', false);
                if (value !== parseInt($input.val(), 10)) {
                    $input.trigger('change');
                    return;
                }
                if (!data.quantity) {
                    location.reload(true);
                    return;
                }
                var $q = $(".my_cart_quantity");
                $q.parent().parent().removeClass("hidden", !data.quantity);
                $q.html(data.cart_quantity).hide().fadeIn(600);

                $input.val(data.quantity);
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
                $("#cart_total").replaceWith(data['website_sale.total']);
            });
        });
    });

});
});
