openerp.so_ready_to_ship = function (instance){

    instance.web.list.columns.add('field.color_on_condition', 'instance.so_ready_to_ship.color_on_condition');
    instance.so_ready_to_ship.color_on_condition = instance.web.list.Column.extend({
        format: function (row_data, options) {
            res = this._super.apply(this, arguments);
            var qty = parseFloat(row_data['product_uom_qty'].value);
            var qty_on_hand = parseFloat(row_data['qty_on_hand'].value);
            if (qty_on_hand >= qty){
                return "<font color='#009933'>"+(res)+"</font>";
            }
            return res
        }
    });

    instance.web.list.columns.add('field.color_on_condition_boolean', 'instance.so_ready_to_ship.color_on_condition_boolean');
    instance.so_ready_to_ship.color_on_condition_boolean = instance.web.list.Column.extend({
        format: function (row_data, options) {
            res = this._super.apply(this, arguments);
            var have_qty = row_data['have_qty'].value
            if (have_qty === true){
                return "<font color='#009933'>"+(res)+"</font>";
            }
            return res
        }
    });
};
