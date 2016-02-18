odoo.define('web_tree_image_zoom.TreeImage', function (require) {

var core = require('web.core');
var data = require('web.data');
var session = require('web.session');

var Class = core.Class;
var QWeb = core.qweb;
var list_widget_registry = core.list_widget_registry;

var Column = Class.extend({
    init: function (id, tag, attrs) {
        _.extend(attrs, {
            id: id,
            tag: tag
        });
        this.modifiers = attrs.modifiers ? JSON.parse(attrs.modifiers) : {};
        delete attrs.modifiers;
        _.extend(this, attrs);

        if (this.modifiers['tree_invisible']) {
            this.invisible = '1';
        } else { delete this.invisible; }
    },
    modifiers_for: function (fields) {
        var out = {};
        var domain_computer = data.compute_domain;

        for (var attr in this.modifiers) {
            if (!this.modifiers.hasOwnProperty(attr)) { continue; }
            var modifier = this.modifiers[attr];
            out[attr] = _.isBoolean(modifier)
                ? modifier
                : domain_computer(modifier, fields);
        }

        return out;
    },
    to_aggregate: function () {
        if (this.type !== 'integer' && this.type !== 'float' && this.type !== 'monetary') {
            return {};
        }
        var aggregation_func = this['group_operator'] || 'sum';
        if (!(aggregation_func in this)) {
            return {};
        }
        var C = function (fn, label) {
            this['function'] = fn;
            this.label = label;
        };
        C.prototype = this;
        return new C(aggregation_func, this[aggregation_func]);
    },
    format: function (row_data, options) {
        options = options || {};
        var attrs = {};
        if (options.process_modifiers !== false) {
            attrs = this.modifiers_for(row_data);
        }
        if (attrs.invisible) { return ''; }

        if (!row_data[this.id]) {
            return options.value_if_empty === undefined
                    ? ''
                    : options.value_if_empty;
        }
        return this._format(row_data, options);
    },
    _format: function (row_data, options) {
        return _.escape(formats.format_value(
            row_data[this.id].value, this, options.value_if_empty));
    }
});

var ColumnBinaryImage = Column.extend({
    /**
     * Return a link to the binary data as a Image
     */
    _format: function (row_data, options) {
            this.session = session;
            if (!row_data[this.id] || !row_data[this.id].value) {
                return '';
            }
            var value = row_data[this.id].value, src;
            if (this.type === 'binary') {
                if (value && value.substr(0, 10).indexOf(' ') === -1) {
                    // The media subtype (png) seems to be arbitrary
                    src = "data:image/png;base64," + value;
                } else {
                    var imageArgs = {
                        model: options.model,
                        field: this.id,
                        id: options.id
                    }
                    if (this.resize) {
                        imageArgs.resize = this.resize;
                    }
                    src = session.url('/web/binary/image', imageArgs);
                }
            } else {
                if (!/\//.test(row_data[this.id].value)) {
                    src = '/web/static/src/img/icons/' + row_data[this.id].value + '.png';
                } else {
                    src = row_data[this.id].value;
                }
            }
            return QWeb.render('ListView.row.image', {widget: this, src: src});
        }
});

list_widget_registry
    .add('field.binary', ColumnBinaryImage);

});
