odoo.define('pos_cafe.pop_ups', function (require) {
    "use strict";

    var core = require('web.core');
    var qweb = core.qweb;
    var gui     = require('point_of_sale.gui');
    var PopupWidget = require('point_of_sale.popups');
    var _t = core._t;
    var models = require('point_of_sale.models');
    var Model = require('web.DataModel');

    var TableListPopup = PopupWidget.extend({
        template: 'TableListPopup',
        previous_screen: 'products',

        show: function(options){
            var self = this;
            this._super();

            this.message = options.message || '';
            this.comment = options.comment || '';
            this.renderElement();
        },

        check_table_have_order_or_not: function(table_id) {
            var orders = this.pos.get('orders').models
            for (var i=0; i < orders.length; i ++) {
                var order = orders[i];
                if (order.table && order.table.id == table_id) {
                    return order
                }
            }
            return null;
        },

        renderElement: function() {
            var self = this;
            this._super();
            this.$('.button.cancel').click(function () {
                self.gui.show_screen(self.previous_screen);
            });
            var current_order = self.pos.get('selectedOrder');
            var current_table = current_order.table
            var tables = this.pos.db.get_table_list();
            var index = null;
            for (var i = 0; i < tables.length; i++) {
                if (current_table && current_table.id == tables[i].id) {
                    index = i;
                }
            }
            var tables_show = [];
            if (index != null) {
                for (var i = 0; i < tables.length; i++) {
                    if (i != index) {
                        tables_show.push(tables[i])
                    }
                }
            }
            var tablewidget = $(qweb.render('TableRecord', {
                widget: this,
                tables: tables_show,
            }));
            this.$('.table-list').append(tablewidget);
            this.$('.button.confirm').click(function () {
                var table_id = parseInt($(this).parent().parent().find('.control-button')[0].value);
                self.moving_table(table_id);
            });
        },

        moving_table: function(table_id) {
            if (!table_id) {
                this.gui.show_popup.show_popup('error',{
                    message: _t('Please select table'),
                });
                return;
            }
            var orders = this.pos.get('orders').models;
            var ordered = this.check_table_have_order_or_not(table_id)
            var table = this.pos.db.get_table_by_id(table_id)
            if (!ordered) {
                var old_order = this.pos.get('selectedOrder');
                var to_order = new models.Order({},{
                    pos: this.pos,
                    temporary: true,
                });
                to_order.setTable(table);
                this.pos.db.set_order_to_table(to_order);
                this.pos.get('orders').add(to_order);
                var old_lines = old_order.get_orderlines()
                for (var i=0; i < old_lines.length; i ++) {
                    var old_line = old_lines[i];
                    to_order.add_product(old_line.product, {
                        price: old_line.price,
                        quantity: old_line.quantity,
                        discount: old_line.discount
                    });
                    var selectedLine = to_order.get_selected_orderline();
                    selectedLine['syncBackEnd'] = old_line.syncBackEnd;
                    selectedLine['state'] = old_line.state;
                }
                this.pos.set({ selectedOrder: to_order });
                old_order.trigger('change', old_order);
                old_order.trigger('change:sync');
                this.pos.db.remove_order_from_table(old_order.uid)
                old_order.destroy({'reason':'abandon'});


            } else {
                var to_order = ordered;
                old_order = this.pos.get('selectedOrder');
                var old_lines = old_order.get_orderlines()
                for (var i=0; i < old_lines.length; i ++) {
                    var old_line = old_lines[i];
                    to_order.moving_table = true;
                    to_order.add_product(old_line.product, {
                        price: old_line.price,
                        quantity: old_line.quantity,
                        discount: old_line.discount
                    });
                    var selectedLine = to_order.get_selected_orderline();
                    selectedLine['syncBackEnd'] = old_line.syncBackEnd;
                    selectedLine['state'] = old_line.state;
                }
                this.pos.set({ selectedOrder: to_order });
                to_order.setTable(table);
                this.pos.db.set_order_to_table(to_order);
                this.pos.db.remove_order_from_table(old_order.uid)
                old_order.destroy({'reason':'abandon'});
                to_order.trigger('change', to_order);
                to_order.trigger('change:sync');

            }
            this.gui.show_screen('products');
        }
    });
    gui.define_popup({name:'tablelistpopup', widget: TableListPopup});

    var MoveProductsPopUp = PopupWidget.extend({
        template: 'MoveProductsPopUp',
        previous_screen: 'products',

        show: function(options){
            var self = this;
            this._super();

            this.message = options.message || '';
            this.comment = options.comment || '';
            this.renderElement();
        },

        check_table_ordered: function(table_id) {
            var orders = this.pos.get('orders').models
            for (var i=0; i < orders.length; i ++) {
                var order = orders[i];
                if (order.table && order.table.id == table_id) {
                    return order
                }
            }
            return null;
        },

        renderElement: function(){
            var self = this;
            this._super();
            this.$('.button.cancel').click(function(){
                self.gui.show_screen(self.previous_screen);
                $('.modal-dialog').addClass('oe_hidden');
            });
            var current_order = self.pos.get('selectedOrder');
            var current_table = current_order.table
            var current_lines = current_order.get_orderlines();
            var tables = self.pos.db.get_table_list();
            var index = null;
            for (var i = 0; i < tables.length; i ++) {
                if (current_table && current_table.id == tables[i].id) {
                    index = i;
                }
            }
            var tables_show = [];
            if (index != null) {
                for (var i=0; i < tables.length; i++) {
                    if (i != index) {
                        tables_show.push(tables[i])
                    }
                }
            }

            // render list lines
            for (var i=0; i < current_lines.length; i ++) {
                var line = current_lines[i];
                var order_uid = line.order.uid;
                var linewidget = $(qweb.render('ProductMoveRecord',{
                    widget: this,
                    line: line,
                    id: line.id,
                    order_uid: order_uid,
                    tables: tables_show,
                }));
                linewidget.data('id', line.id);
                this.$('.product-list').append(linewidget);
            }
            // trigger event click submit()
            this.$('.client-line .submit').click(function() {
                var line_id = parseInt($(this).parent().parent().data('id'));
                var table_id = parseInt($(this).parent().parent().find('.control-button')[0].value);
                var quantity = parseInt($(this).parent().parent().find('.control-button')[1].value);
                var order_uid = $(this).parent().parent().find('.control-button')[2].value;
                self.moving_product(line_id, table_id, quantity, order_uid, $(this));
            });

        },


        moving_product: function(line_id, table_id, quantity, order_uid, button_element) {
            if (!table_id) {
                this.gui.show_popup('error',{
                    message: _t('Please select table'),
                });
                return;
            }

            var orders = this.pos.get('orders').models;
            var ordered = this.check_table_ordered(table_id)
            var table = this.pos.db.get_table_by_id(table_id)
            if (ordered == null) { // transfer to new order
                var from_order = this.pos.get('selectedOrder');
                var to_order = new models.Order({},{
                    pos: this.pos,
                    temporary: true,
                });
                to_order.setTable(table);
                this.pos.db.set_order_to_table(to_order);
                this.pos.get('orders').add(to_order);
                // begin add line
                var from_line = from_order.get_orderlines().find(function (line) {
                    return line.id == line_id;
                })
                if (from_line) {
                    var product = this.pos.db.get_product_by_id(from_line.product.id)
                    to_order.moving_product = true;
                    to_order.add_product(product, {
                        price: from_line.price,
                        quantity: quantity,
                        discount: from_line.discount,
                    })
                    var selectedLine = to_order.get_selected_orderline();
                    selectedLine['syncBackEnd'] = from_line.syncBackEnd;
                    selectedLine.state = from_line.state;
                    if (from_line.quantity <= quantity) {
                        from_order.remove_orderline(from_line);
                    } else {
                        from_line.set_quantity(from_line.quantity - quantity);
                    }
                }
                to_order.trigger('change:sync');

            } else { // transfer to old ordered before
                var transfer_to_order = ordered;
                var old_order = this.pos.get('selectedOrder');
                var old_lines = old_order.get_orderlines()
                var line_move = old_lines.find(function (line) {
                    return line.id == line_id
                });

                if (line_move) {
                    var product = this.pos.db.get_product_by_id(line_move.product.id)
                    transfer_to_order.moving_product = true;
                    transfer_to_order.add_product(product, {
                        price: line_move.price,
                        quantity: quantity,
                        discount: line_move.discount,
                    })
                    var selectedLine = transfer_to_order.get_selected_orderline();
                    selectedLine['syncBackEnd'] = line_move.syncBackEnd;
                    selectedLine.state = line_move.state;
                    if (line_move.quantity <= quantity) {
                        old_order.remove_orderline(line_move);
                    } else {
                        line_move.set_quantity(line_move.quantity - quantity);
                    }
                }
                transfer_to_order.trigger('change:sync');
            }
            button_element.parent().parent().hide();
        },
    });
    gui.define_popup({name:'moveproductspopup', widget: MoveProductsPopUp});

    var MoveProducToKittchenPopUp = PopupWidget.extend({
        template: 'MoveProducToKittchenPopUp',
        previous_screen: 'products',

        renderElement: function(){
            var self = this;
            this._super();
            this.$('.button.cancel').click(function(){
                self.gui.show_screen(self.previous_screen);
            });

            this.$('.button.confirm').click(function() {
                self.send_data_to_kitchen();
            });
        },

        send_data_to_kitchen: function() {
            var currentOrder = this.pos.get('selectedOrder');
            var allLines = currentOrder.get_orderlines();
            var arrayDataSync = [];
            for (var i = 0; i < allLines.length; i++) {
                var line = allLines[i];
                if (line.syncBackEnd == undefined || line.syncBackEnd < line.quantity) {
                    var line = allLines[i];
                    if (line.syncBackEnd == undefined) {
                        arrayDataSync.push({
                            'name': line.product.display_name,
                            'product_id': line.product.id,
                            'table_id': currentOrder.table.id,
                            'qty': line.quantity,
                            'uom_id': line.product.uom_id.id
                        })
                    }
                    if (line.syncBackEnd < line.quantity) {
                        arrayDataSync.push({
                            'name': line.product.display_name,
                            'product_id': line.product.id,
                            'table_id': currentOrder.table.id,
                            'qty': line.quantity - line.syncBackEnd,
                            'uom_id': line.product.uom_id.id
                        })
                    }

                    line['syncBackEnd'] = line.quantity;
                }
            }

            if (arrayDataSync.length > 0) {
                var posKitchen = new Model('pos.kitchen');
                return posKitchen.call('create_from_ui',
                    [_.map(arrayDataSync, function (sync) {
                        return sync;
                    })],
                    undefined,
                    {}
                ).fail(function (error, event) {
                    console.warn('Error push data kitchen to backend: ' + error);
                    console.warn('Error push data kitchen to backend: ' + event);

                }).done(function (returnBE) {
                    console.log('push to backend is Done: ' + returnBE)
                });

            } else {
                this.gui.show_popup('error', {
                    'title': _t("Empty Lines"),
                    'body': _t("Empty line need to send kitchen, please add products the first"),
                });
                return;
            }
        }

    })

    gui.define_popup({name:'moveproducttokitchenpopup', widget: MoveProducToKittchenPopUp});

});
