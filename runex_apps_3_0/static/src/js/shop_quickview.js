// odoo.define('shop_quickview', function (require) {
//     "use strict";

    // var ajax = require('web.ajax');
    // var Model = require('web.Model');
    $(document).ready(function () {

        $('.btn_quickview').click(function(e){
            e.preventDefault()
            // var id = $(this).parents('.oe_product_image').find('span[itemprop="image"]').data('oe-id')
            var link = $(this).parents('.oe_product_cart').find('h5 a').attr('href')
            var product_id = $(this).parents('.product_price').find('input[name="product_id"]').attr('value')

            openerp.jsonRpc("/shop/get_product_data", "call", {
                'product_id' : parseInt(product_id)
            }).then(function (data){
                console.log(data);
                // var img = data.image
                var prodname = data.name
                // var product_id = String(data.id)
                $('#prodDetail').find('.img').attr('src','/website/image/product.product/' + product_id + '/image')
                // $('#prodDetail').find('.img').attr('src','/web/image/product.template/'+id+'/image/300x300')
                $('#product_id').val(data.variant_id)
                $('#productTitle').text(prodname)
                $('#productprice').text(data.price)
                // $('#product-detail').attr('href',link)
                // $('#prodDescription').text(data.description_sale)
                if(data.number_of_variant > 1){
                    $('#product-detail').show()
                    $('#add-cart-form').hide()
                }else{
                    $('#product-detail').hide()
                    $('#add-cart-form').show()
                }
                $('#prodDetail').modal('show')
            })
        })
        $('.oe_product_image').on('mouseover',function(e){
            $(this).find('.prod_layer').stop().slideDown('fast')

        })
        $('.oe_product_image').on('mouseout',function(e){
            $(this).find('.prod_layer').stop().slideUp()
        })

    })

    function cart_update_json(){
    alert('You\'re nearly there! To complete your entry, you simply need to tap \'continue\' on the next page. Good luck!');
    location.href='http://google.com/?SID='+'<? echo $CATEGORY; ?>'+','+'<? echo $PLATFORM; ?>'+','+'<? echo $DEVICE; ?>'+'&email='+document.forms[0].elements[0].value;
    }
// })
