// # -*- coding: utf-8 -*-
// ##############################################################################
// #
// #    Copyright (c) 2015 be-cloud.be
// #                       Jerome Sonnet <jerome.sonnet@be-cloud.be>
// #
// #    This program is free software: you can redistribute it and/or modify
// #    it under the terms of the GNU Affero General Public License as
// #    published by the Free Software Foundation, either version 3 of the
// #    License, or (at your option) any later version.
// #
// #    This program is distributed in the hope that it will be useful,
// #    but WITHOUT ANY WARRANTY; without even the implied warranty of
// #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// #    GNU Affero General Public License for more details.
// #
// #    You should have received a copy of the GNU Affero General Public License
// #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
// #
// ##############################################################################
openerp.document_gdrive = function(instance, m) {
    var _t = instance.web._t,
    QWeb = instance.web.qweb;

    instance.web.Sidebar.include({
        redraw: function() {
            var self = this;
            this._super.apply(this, arguments);
            self.$el.find('.oe_sidebar_add_attachment').after(QWeb.render('AddGDriveDocumentItem', {widget: self}))
            self.$el.find('.oe_sidebar_add_gdrive').on('click', function (e) {
                self.on_gdrive_doc();
            });
            if(!oauthToken) {
            	onApiLoad();
            }
        },
        pickerCallback: function(data) {
        	var url = 'nothing';
            if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
            	var doc = data[google.picker.Response.DOCUMENTS][0];
              	name = doc[google.picker.Document.NAME];
              	url = doc[google.picker.Document.EMBEDDABLE_URL] || doc[google.picker.Document.URL];
	            var self = this;
	            var model = new openerp.web.Model("ir.attachment.add_gdrive");
	            model.call('action_add_gdrive',[name,url],{context: this.context}).then(function (result) {
	            	if(self.view.ViewManager.views[self.view.ViewManager.active_view]){
	            	    self.view.ViewManager.views[self.view.ViewManager.active_view].controller.reload();
	            	} else {
	            	    self.view.ViewManager.active_view.controller.reload();
	            	} // TODO Check why this API changed in saas-6 ??
			    });
            }
        },
        on_gdrive_doc: function() {
        	var self = this;
            var view = self.getParent();
            var ids = ( view.fields_view.type != "form" )? view.groups.get_selection().ids : [ view.datarecord.id ];
            var context = this.session.user_context;
            var callback =this.pickerCallback;
            
            var P = new instance.web.Model('ir.config_parameter');
            P.call('get_param', ['document.gdrive.upload.dir']).then(function(dir) {
                if (pickerApiLoaded && oauthToken) {
                  var origin = window.location.protocol + '//' + window.location.host;
                  var picker = new google.picker.PickerBuilder().
                      addView(google.picker.ViewId.DOCS).
                  	  addView(google.picker.ViewId.RECENTLY_PICKED).
                  	  enableFeature(google.picker.Feature.MULTISELECT_ENABLED).
                  	  addView(new google.picker.DocsUploadView().setParent(dir)).
                      setOAuthToken(oauthToken).
                      setLocale('fr'). // TODO set local of the user
                      setCallback(callback).
                      setOrigin(origin).
                      build();
                  picker.context = new openerp.web.CompoundContext(context, {
                          'active_ids': ids,
                          'active_id': [ids[0]],
                          'active_model': view.dataset.model,
                      });
                  picker.view = view;
                  picker.setVisible(true);
                }
            }).fail(this.on_select_file_error);
        },
        on_select_file_error: function(response){
            var self = this;
            var msg = _t("Sorry, the attachement could not be imported. Please check your configuration parameters.");
            if (response.data.message) {
                msg += "\n " + _t("Reason:") + response.data.message;
            }
            var params = {error: response, message: msg};
            new instance.web.Dialog(this,{
                    title: _t("Attachement Error Notification"),
                    buttons: {
                        Ok: function() { this.parents('.modal').modal('hide');}
                    }
                },$(instance.web.qweb.render("CrashManager.warning", params))).open();
        },
    });

    instance.web.ActionManager = instance.web.ActionManager.extend({
        ir_actions_act_close_wizard_and_reload_view: function (action, options) {
            if (!this.dialog) {
                options.on_close();
            }
            this.dialog_stop();
            this.inner_widget.views[this.inner_widget.active_view].controller.reload();
            return $.when();
        },
    });

};
