odoo.define('account_dashboard_bokeh', function (require) {
"use strict";

var core = require('web.core');
var Model = require('web.Model');
var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;

var ShowCharts = Widget.extend({
    start: function () {
        var self = this;

        self.$el.html(QWeb.render("ShowCharts", {widget: self}));
        return this._super.apply(this, arguments);
    }
});

core.action_registry.add('account_dashboard_bokeh', ShowCharts);



return ShowCharts;

});
