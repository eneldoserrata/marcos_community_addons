odoo.define('pos_cafe.db', function (require) {
    "use strict";

    var db = require('point_of_sale.DB');
    var PosDB = db.PosDB;

    db.include({


        reset_order_from_table_id: function(table_id) {
            var table = this.tables.find(function (table) {
                return table.id == table_id;
            })
            table.order = null;
        },
        // Get all table from cache
        get_table_list: function(){
            var list = [];
            if (this.tables) {
                return this.tables
            }
            else {
                return list
            }

        },
        // Get table json from number of table
        get_table_by_number: function(number) {
            var tables = []
            for (var i=0; i < this.tables.length; i++) {
                var table = this.tables[i];
                if (table.number == number) {
                    tables.push(table)
                }
            }
            return tables
        },
        // Get table json from id of table
        get_table_by_id: function(id){
            var tables = this.tables
            for ( var i = 0; i < tables.length; i++) {
                if (parseInt(id) == tables[i].id) {
                    return tables[i]
                }
            }
        },
        // Set order to table
        set_order_to_table: function(order) {
            var tables = this.tables;
            var table  = tables.find(function(table) {
                return table.id == order.table.id
            })
            table.order = order;
        },
        // Remove order outside table
        remove_order_from_table: function(order_uid) {
            var table = this.tables.find(function (table) {
                if (table.order && table.order.uid == order_uid) {
                    return table;
                }
            })
            if (table) {
                table.order = null;
            }
            return;
        }
    })

})