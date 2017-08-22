odoo.define('pos_cafe.sreen', function (require) {
    "use strict";

    var chrome = require('point_of_sale.chrome');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var qweb = core.qweb;


    var TablesScreenWidget = screens.ScreenWidget.extend({
        template:     'TableScreenWidget',
        show_numpad:     false,
        show_leftpane:   true,
        previous_screen: 'products',

        init: function(parent, options) {
            var search_timeout  = null;
            var self = this;
            this._super(parent,options);
            this.search_handler = function(event){
                clearTimeout(search_timeout);

                var query = this.value;

                search_timeout = setTimeout(function(){
                    self.perform_search(query, event.which === 13);
                },70);
            };
            this.clear_search_handler = function(){
                self.clear_search();
            };
        },

        clear_search: function(){
            var tables = this.pos.db.get_table_list();
            this.renderElement();
            this.show();
        },

        perform_search: function(query, buy_result){
            if(query){
                tables = this.pos.db.get_table_by_number(query)
                this.renderElement(tables);
            }else{
                var tables = this.pos.db.get_table_list();
                this.renderElement(tables);
            }
            this.show();
        },

        show: function() {
            var self = this;
            this._super();
            this.$('.table-list').on('click','.table',function(){
                var table_id = parseInt($(this).data()['id']);
                self.clickTable(table_id);
            });
            var tables = this.pos.db.get_table_list();
            for (var i=0; i < tables.length; i ++) {
                var table = tables[i];
                var el = this.$('.table-total[data-id=' +table.id+ ']');
                if (table.order) {
                    var amount_total = table.order.get_total_with_tax().toFixed(3);
                    el.html("<i style='color:red' class='fa fa-shopping-cart text-center'>" + "  " + amount_total+ "</i>");
                } else {
                    el.html("<i style='color:#2A8152' class='fa fa-shopping-cart text-center'>" +'  0'+ "</i>");
                }
            }
        },

        // Render tables
        renderElement: function(tables){
            var self = this;
            this._super();
            if (!tables) {
                tables = this.pos.db.get_table_list();
            }
            for(var i = 0; i < tables.length; i++){
                var table = tables[i];
                var tablewidget = $(qweb.render('Table',{
                    widget: this,
                    table: table,
                    id: table.id,
                }));
                tablewidget.data('id', table.id);
                this.$('.table-list').append(tablewidget);
            }
            this.$('.back').click(function(){
                self.gui.show_screen(self.previous_screen);
            });

            this.el.querySelector('.searchbox input').addEventListener('keyup',this.search_handler);
            $('.searchbox input', this.el).keypress(function(e){
                e.stopPropagation();
            });
            this.el.querySelector('.search-clear').addEventListener('click',this.clear_search_handler);
        },

        // Event click table
        clickTable: function(table_id){
            var currentOrder = this.pos.get('selectedOrder');
            var table_click = this.pos.db.get_table_by_id(table_id);
            var orders = this.pos.get('orders');
            var order = orders.models.find(function (order) {
                if (order.table) {
                    return order.table.id == table_id;
                }
            });
            if (order) {
                this.pos.set({ selectedOrder: order});
                order.trigger('change', order);
            } else {
                if (!currentOrder.table) {
                    currentOrder.setTable(table_click)
                    this.pos.db.set_order_to_table(currentOrder);
                    this.pos.set({ selectedOrder: currentOrder});
                    currentOrder.trigger('change', currentOrder);
                } else {
                    var new_order = new models.Order({}, {pos: this.pos});
                    new_order.setTable(table_click)
                    this.pos.db.set_order_to_table(new_order);
                    orders.add(new_order)
                    this.pos.set({ selectedOrder: new_order});
                    new_order.trigger('change', new_order);
                }
            }
            this.gui.show_screen('products');

        },
    });

    gui.define_screen({
        'name': 'tables',
        'widget': TablesScreenWidget,
    });

    // Add the TablesScreen to the GUI, and set it as the default screen
    chrome.Chrome.include({
        build_widgets: function(){
            this._super();
            this.gui.set_startup_screen('tables');
            this.gui.set_default_screen('tables');
        },
    });

    chrome.OrderSelectorWidget.include({
        order_click_handler: function(event,$el) {
            this._super(event, $el);
            this.gui.show_screen('products');
        }
    })

    screens.PaymentScreenWidget.extend({
        validate_order: function(options) {
            var order = this.pos.get('selectedOrder');
            if (order.table) {
                this.pos.db.remove_order_from_table(order.uid);
            }
            this._super(options);

        }
    });



});

