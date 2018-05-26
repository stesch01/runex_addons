$(document).ready(function () {

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
});
