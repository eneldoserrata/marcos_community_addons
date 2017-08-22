odoo.define('pos_cafe.buttons', function (require) {
    "use strict";
    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var _t = core._t;

    var ButtonMoveProduct = screens.ActionButtonWidget.extend({
        template: 'ButtonMoveProduct',
        button_click: function(){
            var self = this;
            self.gui.show_popup('moveproductspopup',{
                confirm: function(){
                    self.gui.show_screen('products');
                },
            });

        }
    });

    screens.define_action_button({
        'name': 'ButtonMoveProduct',
        'widget': ButtonMoveProduct,
    });


    var ButtonMoveTable = screens.ActionButtonWidget.extend({
        template: 'ButtonMoveTable',
        button_click: function(){
            var self = this;
            self.gui.show_popup('tablelistpopup',{
                confirm: function(){
                    self.gui.show_screen('products');
                },
            });

        }
    });

    screens.define_action_button({
        'name': 'ButtonMoveTable',
        'widget': ButtonMoveTable,
    });

    var ButtonGoTablesScreen = screens.ActionButtonWidget.extend({
        template: 'ButtonGoTablesScreen',
        button_click: function(){
            this.gui.show_screen('tables');
        }
    });

    screens.define_action_button({
        'name': 'ButtonGoTablesScreen',
        'widget': ButtonGoTablesScreen,
    });

    var ButtonSendKitchen = screens.ActionButtonWidget.extend({
        template: 'ButtonSendKitchen',
        button_click: function(){
            var self = this;
            this.gui.show_popup('moveproducttokitchenpopup',{
                message: _t('Will be send all line to Kitchen.'),
                comment: _t('All lines inside your POS screen will be sending to the Kitchen. Please confirm if you want'),
                confirm: function(){
                    self.gui.show_screen('products');
                },
            });
        },
    });

    screens.define_action_button({
        'name': 'ButtonSendKitchen',
        'widget': ButtonSendKitchen,
    });

    var ButtonResetTable = screens.ActionButtonWidget.extend({
        template: 'ButtonResetTable',
        button_click: function(){
            var self = this;
            this.gui.show_popup('confirm',{
                comment: _t('All Orders will removing, are you sure?'),
                confirm: function(){
                    var orders = self.pos.get('orders');
                    for (var i=0; i < orders.models.length; i ++) {
                        var order_deleting = orders.models[i];
                        if (order_deleting.table) {
                            self.pos.db.remove_order_from_table(order_deleting.uid);
                            var el = $('.table-total[data-id=' + order_deleting.table.id + ']');
                            el.html("<i style='color:#2A8152' class='fa fa-shopping-cart text-center'>" +'  0'+ "</i>");
                        }
                        order_deleting.destroy({'reason':'abandon'});
                    }
                    var selectedOrder = self.pos.get('selectedOrder');
                    if (selectedOrder.table) {
                        self.pos.db.remove_order_from_table(selectedOrder.uid);
                        var el = $('.table-total[data-id=' + selectedOrder.table.id + ']');
                        el.html("<i style='color:#2A8152' class='fa fa-shopping-cart text-center'>" +'  0'+ "</i>");
                    }
                    selectedOrder.destroy({'reason':'abandon'});
                },
            });
        },
    });

    screens.define_action_button({
        'name': 'ButtonResetTable',
        'widget': ButtonResetTable,
    });


    var ButtonCookingDone = screens.ActionButtonWidget.extend({
        template: 'ButtonCookingDone',
        button_click: function(){
            var line = this.pos.get('selectedOrder').get_selected_orderline();
            line.state = 'done';
            line.trigger('change', line);
            line.order.trigger('change:sync');
        },
    });

    screens.define_action_button({
        'name': 'ButtonCookingDone',
        'widget': ButtonCookingDone,
    });

    var ButtonCookingCancel = screens.ActionButtonWidget.extend({
        template: 'ButtonCookingCancel',
        button_click: function(){
            var line = this.pos.get('selectedOrder').get_selected_orderline();
            line.state = 'cancel';
            line.trigger('change', line);
            line.order.trigger('change:sync');
        },
    });

    screens.define_action_button({
        'name': 'ButtonCookingCancel',
        'widget': ButtonCookingCancel,
    });
});