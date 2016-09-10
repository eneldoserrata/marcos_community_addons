odoo.define('web_upload.up_load', function(require) {
    var FormView = require('web.FormView');
    var core = require('web.core');
    var QWeb = core.qweb;

    FormView.include({

        // init: function(parent, dataset, view_id, options) {
        //     this._super(parent, dataset, view_id, options);
        //     this.up_load();
        // },

        // load_record: function(record) {
        //     this._super(record);
        //     this.up_load();
        // },

        // reload: function() {
        //     this._super();
        //     this.up_load();
        // },

        get_selected_ids: function() {
            var id = this._super();
            var model = this.dataset.model
            this.up_load(id, model);
            return id;
        },
        
        up_load: function(id, model) {
            var self = this;
            this.upload = $(QWeb.render("web_upload.MultiUploads", {'id': id, 'model': model}));
            this.$('.upload').replaceWith(this.upload);
            $('#fileupload').fileupload({
                url: '/upload/files',
                dataType: 'json',
                done: function (e, data) {
                    if (data && data.result && data.result.model && data.result.id) {
                        console.log('++++ done +++++')
                        return self.trigger('load_record', self.datarecord);
                        
                    } else {
                        self.trigger('load_record', self.datarecord);
                        return False
                    }
                },
                fail: function(e, data) {
                    console.log('++++ fail +++++')
                    self.trigger('load_record', self.datarecord);
                    return False
                },
            })
                
        }
    });
})