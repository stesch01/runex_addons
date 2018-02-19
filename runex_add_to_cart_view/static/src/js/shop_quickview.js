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
                // console.log(data);
                // var img = data.image
                var prodname = data.name
                // var product_id = String(data.id)
                $('#prodDetail').find('.img').attr('src','/website/image/product.product/' + product_id + '/image')
                // $('#prodDetail').find('.img').attr('src','/web/image/product.template/'+id+'/image/300x300')
                $('#product_id').val(data.variant_id)
                $('#productTitle').text(prodname)
                $('#productprice').text(data.price)
                $('#cart_products > tbody > tr > td.text-center > div > input').val(1);
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

        $('#add-cart-form').submit(function(e) {
            e.preventDefault();
            var product_id = $(this).find('input[name="product_id"]').attr('value');
            var add_qty = $(this).find('input[name="add_qty"]').attr('value');
            $.post( '/shop/cart/update_main',
                    { product_id: parseInt(product_id), add_qty : parseFloat(add_qty)},
                    function(returnedData){
                      var cart_qty = '';
                      var slide;
                      for (var i = 0; i < 20; i++) {
                        slide = returnedData.charAt(i);
                        if (!(isNaN(slide))) {
                          cart_qty = cart_qty + slide;
                        }else{
                          break;
                        }
                      }
                      if (cart_qty){
                        returnedData = returnedData.slice(i + 1);
                      }

                      $('#cart_link > sup').html("<span>" + cart_qty + "</span>");
                      if ($('.dropdown_cart').length){
                        $('.dropdown_cart').replaceWith(returnedData);
                      }else{
                        $("#cart_link").after(returnedData); // add a cart with item
                      }

                      $('#btn_cart').removeClass("hidden");
                    }

                  );
            $('#prodDetail').modal('hide');
            $('#cart_products > tbody > tr > td.text-center > div > input').val(1);
        });
    });
// })
