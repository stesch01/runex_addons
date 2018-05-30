$(document).ready(function () {

    var $products_grid_before = $('#products_grid_before');
    if (!$products_grid_before.length) return;

    var menu_b2b_height = $('#b2b-menu').outerHeight() || 0;

    $products_grid_before.css({
        'position': 'sticky',
        'top': menu_b2b_height,
    });


});

