$(document).ready(function () {

    var $products_grid_before = $('#products_grid_before');
    if (!$products_grid_before.length) return;

    $products_grid_before.css({
        'padding-left': 0,
        'padding-right': 0,
        'width': $products_grid_before.width(),
    });
    var menu_navbar_height = $('#oe_main_menu_navbar').outerHeight() || 0;
    var menu_b2b_height = $('#b2b-menu').outerHeight() || 0;
    var $grid_before_first_child = $products_grid_before.children(":first");
    var grid_before_first_child_padd_marg = parseFloat($grid_before_first_child.css('marginTop')||0)+
        parseFloat($grid_before_first_child.css('paddingTop')||0);
    $products_grid_before.stickySidebar({
        'topSpacing': menu_b2b_height,
        'bottomSpacing': -(grid_before_first_child_padd_marg)-menu_navbar_height,
    });

});

