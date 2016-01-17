odoo.define("web_print.command", function (require) {

    var ListView = require('web.ListView');
    var core = require('web.core');
    var web = require("web.Model");
    var formats = require('web.formats');
    var Model = require('web.DataModel');
    //var QWeb = core.qweb;

    ListView.include({
        render_buttons: function () {
            var self = this;
            var add_button = false;
            if (!this.$buttons) { // Ensures that this is only done once
                add_button = true;
            }
            this._super.apply(this, arguments); // Sets this.$buttons
            if (add_button) {

                this.$buttons.on('click', '.web_print_pdf', function () {
                    self.export_to_excel("excel")
                });

            }
            return this.$buttons;
        },
        export_to_excel: function(export_type) {
            var self = this
            var export_type = export_type
            view = this.getParent()
            // Find Header Element
            header_eles = self.$el.find('.oe_list_header_columns')
            header_name_list = []
            $.each(header_eles,function(){
                $header_ele = $(this)
                header_td_elements = $header_ele.find('th')
                $.each(header_td_elements,function(){
                    $header_td = $(this)
                    text = $header_td.text().trim() || ""
                    data_id = $header_td.attr('data-id')
                    if (text && !data_id){
                        data_id = 'group_name'
                    }
                    header_name_list.push({'header_name': text.trim(), 'header_data_id': data_id})
                   // }
                });
            });

            //Find Data Element
            data_eles = self.$el.find('.oe_list_content > tbody > tr')
            export_data = []
            $.each(data_eles,function(){
                data = []
                $data_ele = $(this)
                is_analysis = false
                if ($data_ele.text().trim()){
                //Find group name
	                group_th_eles = $data_ele.find('th')
	                $.each(group_th_eles,function(){
	                    $group_th_ele = $(this)
	                    text = $group_th_ele.text().trim() || ""
	                    is_analysis = true
	                    data.push({'data': text, 'bold': true})
	                });
	                data_td_eles = $data_ele.find('td')
	                $.each(data_td_eles,function(){
	                    $data_td_ele = $(this)
	                    text = $data_td_ele.text().trim() || ""
	                    if ($data_td_ele && $data_td_ele[0].classList.contains('oe_number') && !$data_td_ele[0].classList.contains('oe_list_field_float_time')){
	                        text = text.replace(/[^0-9]/g, '');
	                        text = formats.parse_value(text, { type:"float" }, 0.0);
	                        data.push({'data': text || "", 'number': true})
	                    }
	                    else{
	                        data.push({'data': text})
	                    }
	                });
	                export_data.push(data)
                }
            });

            //Find Footer Element

            footer_eles = self.$el.find('.oe_list_content > tfoot> tr')
            $.each(footer_eles,function(){
                data = []
                $footer_ele = $(this)
                footer_td_eles = $footer_ele.find('td')
                $.each(footer_td_eles,function(){
                    $footer_td_ele = $(this)
                    text = $footer_td_ele.text().trim() || ""
                    if ($footer_td_ele && $footer_td_ele[0].classList.contains('oe_number')){
                        text = text.replace(/[^0-9]/g, '');
                        text = formats.parse_value(text, { type:"float" }, 0.0);
                        data.push({'data': text || "", 'bold': true, 'number': true})
                    }
                    else{
                        data.push({'data': text, 'bold': true})
                    }
                });
                export_data.push(data)
            });

            //Export to excel
            $.blockUI();
            if (export_type === 'excel'){
                 view.session.get_file({
                     url: '/web/export/zb_excel_export',
                     data: {data: JSON.stringify({
                            model : view.model,
                            headers : header_name_list,
                            rows : export_data,
                     })},
                     complete: $.unblockUI
                 });
             }
             else{
                console.log(view)
                new Model("res.users").get_func("read")(this.session.uid, ["company_id"]).then(function(res) {
                    new Model("res.company").get_func("read")(res['company_id'][0], ["name"]).then(function(result) {
                        view.session.get_file({
                             url: '/web/export/zb_pdf_export',
                             data: {data: JSON.stringify({
                                    uid: view.session.uid,
                                    model : view.model,
                                    headers : header_name_list,
                                    rows : export_data,
                                    company_name: result['name']
                             })},
                             complete: $.unblockUI
                         });
                    });
                });
             }
        },

    });


});
