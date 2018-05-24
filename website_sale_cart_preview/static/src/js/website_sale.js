$(document).ready(function () {

    var shopping_cart_link = $('ul#top_menu li > a[href$="/shop/cart"]');
    var shopping_cart_link_counter;
    shopping_cart_link.on("mouseenter",function () {
        var self = this;
        clearTimeout(shopping_cart_link_counter);
        $content = $('#add_to_cart_preview').find('.dropdown-content');
        $content.hide();
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
        var self = this;
        setTimeout(function () {
            $content = $('#add_to_cart_preview').find('.dropdown-content');
            if(!$content.is(':hover') && !$(self).is(':hover')) {
                $content.hide();
            }
        }, 100);
    });
});
