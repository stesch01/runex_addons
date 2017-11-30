openerp.so_ready_to_ship = function (instance){

    instance.web.list.columns.add('field.color_on_condition', 'instance.so_ready_to_ship.color_on_condition');
    instance.so_ready_to_ship.color_on_condition = instance.web.list.Column.extend({
        format: function (row_data, options) {
            res = this._super.apply(this, arguments);
            var order_ref = (row_data['order_id'].value[1])
            var qty = parseFloat(row_data['product_uom_qty'].value);
            var qty_on_hand = parseFloat(row_data['qty_on_hand'].value);
            if (qty_on_hand >= qty){
                return "<strong><font color='#009933'>"+(order_ref)+"</font></strong>";
            }
            return order_ref
        }
    });

    instance.web.list.columns.add('field.color_on_condition_boolean', 'instance.so_ready_to_ship.color_on_condition_boolean');
    instance.so_ready_to_ship.color_on_condition_boolean = instance.web.list.Column.extend({
        format: function (row_data, options) {
            res = this._super.apply(this, arguments);
            var have_qty = row_data['have_qty'].value
            if (have_qty === true){
                return "<strong><font color='#009933'>"+(res)+"</font></strong>";
            }
            return res
        }
    });
};
