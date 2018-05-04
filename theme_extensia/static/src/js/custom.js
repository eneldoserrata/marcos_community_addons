odoo.define('pappaya.custom', function (require) {
"use strict";
console.log('Pappaya JS');

    //~ $(document).ready(function () {
        //~ // Add active class in menu parent
        //~ $('.oe_menu_leaf').on('click', function() {
            //~ var $items = $(this).parents('li');
            //~ setTimeout(function(){
                //~ $items.addClass('active');
            //~ }, 300);
        //~ });
    //~ });

    // Override controlpanel styling
    var controlPanel = require('web.ControlPanel');
    controlPanel.include({
        //~ _update_search_view: function(searchview, is_hidden) {
            //~ if (searchview) {
                //~ searchview.$buttons = this.nodes.$searchview_buttons;
                //~ searchview.toggle_visibility(!is_hidden);
                //~ // Set title based on current breadcrumb
                //~ this.$title_col.html(this.nodes.$breadcrumbs.find('.active').html());
            //~ }
        //~ }
    });

});
