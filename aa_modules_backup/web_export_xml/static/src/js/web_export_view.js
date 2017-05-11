/*
# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
*/
odoo.define('web_export_xml', function (require) {
'use strict';


    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;
    var Sidebar = require('web.Sidebar');

    Sidebar.include({
        redraw: function () {
            var self = this;
            this._super.apply(this, arguments);
            if (self.getParent().ViewManager.active_view == 'list') {
                self.$el.find('.oe_sidebar').append(QWeb.render('AddExportViewMain', {widget: self}));
                self.$el.find('.oe_sidebar_export_xml').on('click', self.on_sidebar_export_xml);
            }
        },

        on_sidebar_export_xml: function () {
            // Select the first list of the current (form) view
            // or assume the main view is a list view and use that
            var self = this,
                view = this.getParent(),
                children = view.getChildren();
            if (children) {
                children.every(function (child) {
                    if (child.field && child.field.type == 'one2many') {
                        view = child.viewmanager.views.list.controller;
                        return false; // break out of the loop
                    }
                    if (child.field && child.field.type == 'many2many') {
                        view = child.list_view;
                        return false; // break out of the loop
                    }
                    return true;
                });
            }
            var export_columns_keys = [];
            var export_columns_names = [];
            $.each(view.visible_columns, function () {
                if (this.tag == 'field') {
                    // non-fields like `_group` or buttons
                    export_columns_keys.push(this.id);
                    export_columns_names.push(this.string);
                }
            });
            var rows = view.$el.find('.oe_list_content > tbody > tr');
            var export_rows = [];
            $.each(rows, function () {
                var $row = $(this);
                // find only rows with data
                if ($row.attr('data-id')) {
                    var export_row = [];
                    var checked = $row.find('th input[type=checkbox]').attr("checked");
                    if (children && checked === "checked") {
                        $.each(export_columns_keys, function () {
                            var cell = $row.find('td[data-field="' + this + '"]').get(0);
                            var text = cell.text || cell.textContent || cell.innerHTML || "";
                            if (cell.classList.contains("oe_list_field_float")) {
                                export_row.push(instance.web.parse_value(text, {'type': "float"}));
                            }
                            else if (cell.classList.contains("oe_list_field_boolean")) {
                                var data_id = $('<div>' + cell.innerHTML + '</div>');
                                if (data_id.find('input').get(0).checked) {
                                    export_row.push(_t("True"));
                                }
                                else {
                                    export_row.push(_t("False"));
                                }
                            }
                            else if (cell.classList.contains("oe_list_field_integer")) {
                                var tmp2 = text;
                                do {
                                    var tmp = tmp2;
                                    tmp2 = tmp.replace(instance.web._t.database.parameters.thousands_sep, "");
                                } while (tmp !== tmp2);

                                export_row.push(parseInt(tmp2));
                            }
                            else {
                                export_row.push(text.trim());
                            }
                        });
                        export_rows.push(export_row);
                    }
                }
            });
            $.blockUI();
            view.session.get_file({
                url: '/web/export/xml',
                data: {data: JSON.stringify({
                    model: view.model,
                    rows: export_rows
                })},
                complete: $.unblockUI
            });
        }
    });

});
