odoo.define('inputmask_widgets', function (require) {
    "use strict";
    var form_widgets = require('web.form_widgets');
    var core = require('web.core');
    var FieldMask = form_widgets.FieldChar.extend({
        template: "FieldMask",
        attributes: {},
        init: function (field_manager, node) {
            this._super(field_manager, node)
            var keyMask = 'data-inputmask';
            if (keyMask in node.attrs)
                this.attributes[keyMask] = node.attrs[keyMask];
            else
                this.attributes = Object.keys(node.attrs).reduce(function (filtered, key) {
                    if (key.indexOf(keyMask) !== -1)
                        filtered[key] = node.attrs[key];
                    return filtered;
                }, {});
            if (!this.attributes)
                console.warn("The widget Mask expects the 'data-inputmask[-attribute]' attributes!")
        },
        render_value: function (mask) {
            this._super();
            if (this.$input !== undefined && this.attributes) {
                this.$input.inputmask(mask);
            }
        },
    });
    var FieldMaskRegex = FieldMask.extend({
        render_value: function () {
            this._super("Regex");
        }
    });

    core.form_widget_registry.add('mask', FieldMask);
    core.form_widget_registry.add('mask_regex', FieldMaskRegex);
    return {FieldMask: FieldMask, FieldMaskRegex: FieldMaskRegex};
});
