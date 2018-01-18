odoo.define('document_thumbnail', function (require) {
"use strict";

var core = require('web.core');
var Sidebar = require('web.Sidebar');

var _t = core._t;

Sidebar.include({
    start : function(){
        var self = this;
        self._super.apply(self, arguments);
        self.$el.on('click','.o_sidebar_thumbnail_attachment', function(evt) {
            self.do_action({
                name: _t('Attachment Thumbnails'),
                type: 'ir.actions.act_window',
                target: 'new',
                flags: {
                    read_only_mode: true
                },
                res_model: 'ir.attachment',
                domain: [
                    '&',
                    ['res_model', '=', self.dataset.model],
                    ['res_id', '=', self.model_id]
                ],
                view_mode: 'kanban',
                view_type: 'form',
                views: [
                    [false, 'kanban']
                ]
            });
            evt.preventDefault();
        });
    }
});

});