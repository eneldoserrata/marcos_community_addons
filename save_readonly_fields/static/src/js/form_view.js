odoo.define('save_readonly_fields.update_form_view', function (require) {
    "use strict";

    var FormView = require('web.FormView');

    // This method is overwritten to allow save for readonly fields...
    FormView.include({
        _process_save: function(save_obj) {
            var self = this;
            var prepend_on_create = save_obj.prepend_on_create;
            var def_process_save = $.Deferred();
            try {
                var form_invalid = false,
                    values = {},
                    first_invalid_field = null,
                    readonly_values = {},
                    deferred = [];

                $.when.apply($, deferred).always(function () {

                    _.each(self.fields, function (f) {
                        if (!f.is_valid()) {
                            form_invalid = true;
                            if (!first_invalid_field) {
                                first_invalid_field = f;
                            }
                        } else if (f.name !== 'id' && (!self.datarecord.id || f._dirty_flag)) {
                            // Special case 'id' field, do not save this field
                            // on 'create' : save all non readonly fields
                            // on 'edit' : save non readonly modified fields
                            if (!f.get("readonly")) {
                                values[f.name] = f.get_value(true);
                            } else {
                                values[f.name] = f.get_value(true);
                                readonly_values[f.name] = f.get_value(true);
                            }
                        }

                    });

                    // Heuristic to assign a proper sequence number for new records that
                    // are added in a dataset containing other lines with existing sequence numbers
                    if (!self.datarecord.id && self.fields.sequence &&
                        !_.has(values, 'sequence') && !_.isEmpty(self.dataset.cache)) {
                        // Find current max or min sequence (editable top/bottom)
                        var current = _[prepend_on_create ? "min" : "max"](
                            _.map(self.dataset.cache, function(o){return o.values.sequence})
                        );
                        values['sequence'] = prepend_on_create ? current - 1 : current + 1;
                    }
                    if (form_invalid) {
                        self.set({'display_invalid_fields': true});
                        first_invalid_field.focus();
                        self.on_invalid();
                        def_process_save.reject();
                    } else {
                        self.set({'display_invalid_fields': false});
                        var save_deferral;
                        if (!self.datarecord.id) {
                            // Creation save
                            save_deferral = self.dataset.create(values, {readonly_fields: readonly_values}).then(function(r) {
                                self.display_translation_alert(values);
                                return self.record_created(r, prepend_on_create);
                            }, null);
                        } else if (_.isEmpty(values)) {
                            // Not dirty, noop save
                            save_deferral = $.Deferred().resolve({}).promise();
                        } else {
                            // Write save
                            save_deferral = self.dataset.write(self.datarecord.id, values, {readonly_fields: readonly_values}).then(function(r) {
                                self.display_translation_alert(values);
                                return self.record_saved(r);
                            }, null);
                        }
                        save_deferral.then(function(result) {
                            def_process_save.resolve(result);
                        }).fail(function() {
                            def_process_save.reject();
                        });
                    }
                });
            } catch (e) {
                console.error(e);
                return def_process_save.reject();
            }
            return def_process_save;
        },
    });
});