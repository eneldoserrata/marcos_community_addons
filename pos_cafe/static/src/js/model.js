odoo.define('pos_cafe.models', function (require) {
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');

    var _superPosModel = models.PosModel;
    models.PosModel = models.PosModel.extend({
        create_order: function(order){
            var self = this,
                model = null;
            this._super(order);
            model = self.get('selectedOrder');
            self.fetch('pos.order', ['table_id'], [['id', '=', model.get('order_id')]])
                .then(function(table_data) {
                    var table = self.db.get_table_by_id(table_data[0].table_id[0]);
                    model.setTable(table);
                    model.set_screen_data('cashier_screen', 'products');
                });
        },

        // Remove cache order inside tables db
        delete_current_order: function(){
            var order = this.get('selectedOrder')
            if (order.table) {
                this.db.remove_order_from_table(order.uid);
            }
            _superPosModel.prototype.delete_current_order.call(this);

        },
        // Get image of table filter id
        get_image: function(table_id) {
            if (table_id != undefined) {
                return window.location.origin + '/web/binary/image?model=pos.table&field=image&id=' + table_id;
            }
            else {
                return ''
            }
        },

        // Return table name
        get_table_name: function(){
            var order = this.get('selectedOrder')
            var table = order.table;
            return table ? table.name : "";
        },
    });

    models.load_models([
        {
            model: 'pos.config',
            fields: ['table_ids', 'kitchen'],
            domain: function(self) {return [['id','=', self.pos_session.config_id[0]]]},
            context:{},
            loaded: function(self, tables){
                for (var i=0; i < tables.length; i ++) {
                    self.table_ids = tables[i].table_ids;
                    self.kitchen = tables[i].kitchen;
                    break;
                }
            },
        },
        {
            model: 'pos.table',
            fields: ['id', 'number', 'name', 'capacity'],
            domain: function(self) {return [['id','in', self.table_ids]]},
            context:{},
            loaded: function(self, tables){
                for (var i = 0; i < tables.length; i ++) {
                    tables[i].image_url = self.get_image(tables[i].id)
                }
                self.db.tables = tables;
            },
        }
    ]);

    var _super_order = models.Order;
    models.Order = models.Order.extend({

        // i loading table from cache datas and re-render again
        init_from_JSON: function (json) {
            _super_order.prototype.init_from_JSON.apply(this,arguments);
            if (json.table) {
                table = this.pos.db.get_table_by_id(json.table.id)
                this.setTable(table);
                this.pos.db.set_order_to_table(this)
            }
        },

        export_for_printing: function(){
            var json = _super_order.prototype.export_for_printing.call(this);
            var table = this.get('table');
            if (typeof table !== 'undefined') {json.table = table.name;}
            return json;
        },

        // i save data table to cache
        export_as_JSON: function() {
            var json = _super_order.prototype.export_as_JSON.call(this);
            table = this.get('table');
            if (table) {
                json.tb_id = table.id
                json.table = {
                    capacity: table.capacity,
                    id: table.id,
                    name: table.name,
                    number: table.number
                }
            }
            if (this.moving_product) {
                json.moving_product = true;
            }
            if (this.moving_table) {
                json.moving_table = true;
            }
            return json;
        },

        setTable: function(table){
            this.set({table: table});
            this.table = table;

        },

        remove_order: function(){
            _super_order.prototype.remove_order.call(this);
            this.pos.pos_bus.updating_table({'tables': this.pos.db.get_table_list()});
        },
        get_table: function(){
            return this.get('table');
        },

        get_image: function() {
            var table = this.get('table');
            if (table) {
                return window.location.origin + '/web/binary/image?model=pos.table&field=image&id=' + this.get('table').id;
            }
            else {
                return ''
            }
        }
    });

    var _supoerOrderLine = models.Orderline;
    models.Orderline = models.Orderline.extend({
        initialize: function(){
            _supoerOrderLine.prototype.initialize.apply(this, arguments);

        },

        init_from_JSON: function (json) {
            if (json.state) {
                this.state = json.state;
            }
            _supoerOrderLine.prototype.init_from_JSON.apply(this,arguments);

        },

        export_as_JSON: function(){
            var json = _supoerOrderLine.prototype.export_as_JSON.apply(this, arguments);
            if (this.state) {
                json.state = this.state;
            }
            return json;
        },
    });

});