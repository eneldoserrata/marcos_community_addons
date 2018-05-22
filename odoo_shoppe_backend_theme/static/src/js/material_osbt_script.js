odoo.define('odoo_shoppe_backend_theme.material_osbt_script', function (require) {
"use strict";

require('web.dom_ready');
var core = require('web.core');
var WebClient = require('web.WebClient');
var ControlPanel = require('web.ControlPanel');
var Widget = require('web.Widget');
var ajax = require('web.ajax');
var utils = require('web.utils');
var rpc = require('web.rpc');
// var Model = require('web.DataModel');
var session = require('web.session');
var UserMenu = require('web.UserMenu');
var SearchView = require('web.SearchView');
var SystrayMenu = require('web.SystrayMenu');
var data = require('web.data');
// var KanbanView = require('web_kanban.KanbanView');
var local_storage = require('web.local_storage');
var Dialog = require('web.Dialog');
var time = require('web.time');
// var FormRelational = require('web.form_relational');
var date_time_format = false;
var date_time_format_lang = false;

var qweb = core.qweb;
// var FieldRadio = core.form_widget_registry.get('radio');
var relational_fields = require('web.relational_fields');
var FieldRadio = relational_fields.FieldRadio;
var field_registry = require('web.field_registry');

// var ThemeRadio = FieldRadio.extend({
//     'template': 'FieldThemeRadio',
//     render_value: function () {
//         this._super.apply(this, arguments);
//         if(this.get('effective_readonly')) {
//             this.$el.attr('id', this.get('value')? 'theme_' + this.get('value')[0] : "");
//         }
//         // var self = this;
//         // this.$el.toggleClass("oe_readonly", this.get('effective_readonly'));
//         // this.$("input").prop("checked", false).filter(function () {return this.value == self.get_value();}).prop("checked", true);
//         // this.$(".oe_radio_readonly").css({'' this.get('value') ? this.get('value')[1] : "");
//     } 
// });

//core.form_widget_registry.add('theme_radio', ThemeRadio);
//field_registry.add('theme_radio', ThemeRadio);


var ThemeSwicher =  Widget.extend({
        template: "theme-switcher",
        theme_cookie_name: "material_theme",
        events: {
            'click .switch_style': 'switch_style'
        },
        open_themes: function() {
            var self = this;
            // TODO: I am a mess refactor me
            if(this.$('.theme-switcher').hasClass("active")){
                this.$('.theme-switcher').animate({"right":"-350px"}, function(){
                    self.$('.theme-switcher').toggleClass("active");
                });
            }else{
                this.$('.theme-switcher').animate({"right":"0px"}, function(){
                    self.$('.theme-switcher').toggleClass("active");
                });
            }
        },
        switch_style: function(ev){
            ev.preventDefault();
            var theme = $(ev.currentTarget).data('theme');
            this.switch_theme(theme);
        },
        switch_theme: function(theme){
            var links = $('link[rel*=style][theme]');
            if (theme){
                var activate_me = links.filter(function(){ return $(this).attr('theme') === theme;});
                var inactive_others = links.filter(function(){ return $(this).attr('theme') !== theme;});
                // First enable theme
                activate_me.prop('disabled', false);
                // TODO: to stop flickring I think we should use <link rel= preload or alternate instead of
                // settimout may be it works. give it try when you have time
                setTimeout(function(){
                    inactive_others.prop('disabled', true);
                }, 40);
                rpc.query({
                    model: 'res.users', method: 'color_switcher_write',
                    args: [[session.uid], theme]
                });
            }
        }
    });

var SystrayThemeSwitcher = Widget.extend({
    template:'ThemeSwicherSysTray',
    events: {
        'click .theme-switcher-toggler': 'toggle_themes',
    },
    init:function(){
        var self = this;
        var theme_switcher = new ThemeSwicher();

        rpc.query({
            model: 'res.users', method: 'read',
            args: [[session.uid], ['theme', 'hide_theme_switcher', 'theme_lables_color', 'company_id']]
        }).then(function (res) {
            theme_switcher.switch_theme(res[0].theme);
            theme_switcher.appendTo($('.o_main_content'));
            self.theme_switcher = theme_switcher;
            if(res[0].hide_theme_switcher == false){
                self.$el.remove();
            }
            rpc.query({
                model: 'res.company', method: 'read',
                args: [[res[0].company_id[0]], ['theme_lables_color']]
            }).then(function(res_company){
                $('head').append('<style >label {color: '+ res_company[0].theme_lables_color +';}</style >');
            });
        });
    },
    toggle_themes: function(ev){
        ev.preventDefault();
        var self = this;
        this.theme_switcher.open_themes();
    },
 
});
SystrayMenu.Items.push(SystrayThemeSwitcher);

var TopMenu =  Widget.extend({
    start: function() {
        var self = this;
        this.$el.on('click', 'a[data-menu]', function(ev) {
            ev.preventDefault();
            var fnc = self['on_menu_' + $(this).data('menu')];
            if (fnc) {
                fnc($(this));
            }
        });
    },
    on_menu_action_home_inbox: function() {
        this.getParent().action_manager.do_action('mail.action_mail_inbox_feeds');
    },
    on_menu_action_compose_mail: function() {
        this.getParent().action_manager.do_action('mail.action_email_compose_message_wizard');
    },
    on_menu_action_calender: function() {
        this.getParent().action_manager.do_action('calendar.action_calendar_event');
    },
    on_menu_action_partner_map: function() {
        var partner_url = document.location.origin + '/partners/map';
        window.open(partner_url, '_blank');
    },
});

ControlPanel.include({
    start: function() {
        var self = this;
        this.$el.on('click', 'a.toogle_control_panel', function(ev) {
            ev.preventDefault();
            console.log('clickable');
            if ($('.o_control_panel ol.breadcrumb').is(':visible'))
                $('.o_control_panel ol.breadcrumb, .o_control_panel .o_cp_searchview, .o_control_panel .o_cp_left, .o_control_panel .o_cp_right').slideUp(500);
            else
                $('.o_control_panel ol.breadcrumb, .o_control_panel .o_cp_searchview, .o_control_panel .o_cp_left, .o_control_panel .o_cp_right').slideDown(500);
        });
        return this._super.apply(this, arguments);
    }
});

SearchView.include({
    events: _.extend({}, SearchView.prototype.events, {
        'click .o_searchview_more': function (e) {
            $(e.target).toggleClass('fa-caret-up fa-caret-down');
            var visible_search_menu = (local_storage.getItem('visible_search_menu') !== 'true');
            local_storage.setItem('visible_search_menu', visible_search_menu);
            this.toggle_buttons();
        }
    }),
    start: function(){
        this._super.apply(this, arguments);
        this.$('.o_searchview_more')
            .toggleClass('fa-caret-down', this.visible_filters)
            .toggleClass('fa-caret-up', !this.visible_filters);
    },
    toggle_visibility: function (is_visible) {
        this.do_toggle(!this.headless && is_visible);
        if (this.$buttons) {
            this.$buttons.toggle(!this.headless && is_visible && this.visible_filters);
        }
    },
});

UserMenu.include({
    start: function() {
    var self = this;
        this.$el.on('click', 'a[data-menu]', function(ev) {
            ev.preventDefault();
            var f = self['on_menu_' + $(this).data('menu')];
            if (f) {
                f($(this));
            }
        });
        this.$el.parent().show();
        return this._super.apply(this, arguments);
    },
    do_update: function () {
        var self = this;
        if (!session.uid)
                return;
        var $lang_icon = self.$el.find('a[data-menu="settings"] img');
        rpc.query({
            model: 'res.company', method: 'read',
            args: [[session.company_id], ['flag', 'flag_image']]
        }).then(function (res) {
            if(res[0].flag == "company_flag"){
                if(res[0].flag_image){
                    $lang_icon.attr('src', 'data:image/jpeg;base64;,' + res[0].flag_image);
                }
                else{
                    $lang_icon.attr('src', '/odoo_shoppe_backend_theme/static/src/img/flag/Thumb_17E1T8XGDEJL4Z8.jpg');
                } 
            }
            else{
                rpc.query("res.users", "get_country_flag", [session.uid]).then(function(res){
                    if(res){
                        $lang_icon.attr('src', 'data:image/jpeg;base64;,' + res);
                    }
                    else{
                        $lang_icon.attr('src', '/odoo_shoppe_backend_theme/static/src/img/flag/Thumb_17E1T8XGDEJL4Z8.jpg');
                    }
                });
            }
        });

        rpc.query({
            model: 'res.users', method: 'get_user_time_format',
            args: [[session.uid], []]
        }).then(function (res) {
            date_time_format = res['time_format'];
            date_time_format_lang = res['time_format_lang'];
        });
        
    },

});


var LeftUserMenu =  UserMenu.extend({
    template: "UserLeft",
    events: {
        'click .oe_topbar_avatar': 'click_on_avatar'
    },
    init: function(parent) {
        this._super(parent);
        this.update_promise = $.Deferred().resolve();
    },
    // start: function() {
    //     var self = this;
    //     this.$el.on('click', 'li a[data-menu]', function(ev) {
    //         ev.preventDefault();
    //         var f = self['on_menu_' + $(this).data('menu')];
    //         if (f) {
    //             f($(this));
    //         }
    //     });
    //     this.$el.parent().show();
    //     return this._super.apply(this, arguments);
    // },
    do_update: function () {
        var $avatar = this.$('.oe_topbar_avatar');
        if (!session.uid) {
            $avatar.attr('src', $avatar.data('default-src'));
            return $.when();
        }
        var topbar_name = session.name;
        if(session.debug) {
            topbar_name = _.str.sprintf("%s (%s)", topbar_name, session.db);
        }
        this.$('.oe_topbar_name').text(topbar_name);
        var avatar_src = session.url('/web/image', {model:'res.users', field: 'image_small', id: session.uid});
        $avatar.attr('src', avatar_src);
        // this.update_promise = this.update_promise.then(fct, fct);
    },
    click_on_avatar: function(){
        var is_mobile = $(window).width() < 768;
        if(is_mobile){
            this.on_menu_settings();
        }else {
            this.$('#user_name').click();
        }
    },
    on_menu_about: function () {
        var self = this;
        var help = ""
        rpc.query("res.company", 'about_company_data', [{}]).then(function (result) {
            help = result;
        });
        setTimeout(function(){
                new Dialog(self, {
                size: 'medium',
                dialogClass: 'o_act_window',
                title: "About",
                $content: help
            }).open();
            },1000);
    },


    // on_menu_settings: function() {
    //     var self = this;
    //     this.getParent().clear_uncommitted_changes().then(function() {
    //         self.rpc("/web/action/load", { action_id: "base.action_res_users_my" }).done(function(result) {
    //             result.res_id = session.uid;
    //             self.getParent().action_manager.do_action(result);
    //         });
    //     });
    // },
    // on_menu_logout: function() {
    //     this.trigger('user_logout');
    // },
    // on_menu_documentation: function () {
    //     window.open('https://www.odoo.com/documentation/user', '_blank');
    // },
    
});

WebClient.include({
    show_application: function() {
        var self = this;
        var res = this._super.apply(this, arguments);
        var topmenu = new TopMenu(this);
        topmenu.setElement(this.$('.user_top_header_menu'));
        topmenu.start();

        // Create the user Left
        self.user_left = new LeftUserMenu(self);
        var user_left_loaded = self.user_left.appendTo(this.$el.find('div.user'));
        // self.user_left.on('user_logout', self, self.on_logout);
        self.user_left.do_update();
        return res;
    },
});

// KanbanView.include({
//     postprocess_m2m_tags: function(records) {
//         var self = this;
//         if (!this.many2manys.length) {
//             return;
//         }
//         var relations = {};
//         records = records ? (records instanceof Array ? records : [records]) :
//                   this.grouped ? Array.prototype.concat.apply([], _.pluck(this.widgets, 'records')) :
//                   this.widgets;

//         records.forEach(function(record) {
//             self.many2manys.forEach(function(name) {
//                 var field = record.record[name];
//                 var $el = record.$('.oe_form_field.o_form_field_many2manytags[name=' + name + ']');
//                 // fields declared in the kanban view may not be used directly
//                 // in the template declaration, for example fields for which the
//                 // raw value is used -> $el[0] is undefined, leading to errors
//                 // in the following process. Preventing to add push the id here
//                 // prevents to make unnecessary calls to name_get
//                 if (! $el[0]) {
//                     return;
//                 }
//                 if (!relations[field.relation]) {
//                     relations[field.relation] = { ids: [], elements: {}, context: self.m2m_context[name]};
//                 }
//                 var rel = relations[field.relation];
//                 field.raw_value.forEach(function(id) {
//                     rel.ids.push(id);
//                     if (!rel.elements[id]) {
//                         rel.elements[id] = [];
//                     }
//                     rel.elements[id].push($el[0]);
//                 });
//             });
//         });
//        _.each(relations, function(rel, rel_name) {
//             var dataset = new data.DataSetSearch(self, rel_name, self.dataset.get_context(rel.context));
//             dataset.read_ids(_.uniq(rel.ids), ['name', 'color']).done(function(result) {
//                 result.forEach(function(record) {
//                     // Does not display the tag if color = 0
//                     if (record.color){
//                         var $tag = $('<span>')
//                             .addClass('o_tag o_tag_color_' + record.color)
//                             .attr('title', _.str.escapeHTML(record.name))
//                             .text(_.str.escapeHTML(record.name));
//                         $(rel.elements[record.id]).append($tag);
//                     }
//                 });
//                 // we use boostrap tooltips for better and faster display
//                 self.$('span.o_tag').tooltip({delay: {'show': 50}});
//             });
//         });
//     },
// });
// FormRelational.FieldMany2ManyTags.include({
//     open_color_picker: function(ev){
//         var self = this;
//         this._super(ev);
//         if (this.fields.color) {
//             _.each(self.$el.children(), function(ee){
//                  $(ee).removeClass('open');
//             })
//             $(ev.currentTarget).toggleClass('open');
//         }
//     },
// });
$(document).ready(function(){

    $('.toggle-slidebar').on('click', function(){
        // collepse all open menu when switch to iconic menu
        $('.cssmenu').find('h3').removeClass('active fix_active');
        $('.cssmenu').find('div.oe_secondary_menu').hide();

        var windowsize = $window.width();
        var leftbar = $('div.o_sub_menu');
        if (windowsize < 768)
            if (leftbar.is(':visible'))
                leftbar.hide();
            else
                leftbar.show();
        else {
            leftbar.show();
        }
        if (leftbar.hasClass('fix_icon_width')) {
            $('div.o_sub_menu.fix_icon_width').removeClass('fix_icon_width');
            leftbar.find('.menu_heading').removeClass('iconic_menu_heading');
            leftbar.find('.oe_secondary_menu').removeClass('iconic_menu');
            leftbar.find('.o_sub_menu_footer').show();

            utils.set_cookie('side_menu', JSON.stringify({
                'odooshoppe_menu': 'full'}), 2592000);
        } else {
            leftbar.addClass('fix_icon_width');
            leftbar.find('.menu_heading').addClass('iconic_menu_heading');
            leftbar.find('.oe_secondary_menu').hide().addClass('iconic_menu');
            leftbar.find('.o_sub_menu_footer').hide();
            utils.set_cookie('side_menu', JSON.stringify({
                'odooshoppe_menu': 'collapse'}), 2592000);
        }
    });

    //Type 1
    $('.cssmenu > h3').click(function() {
        $('.cssmenu h3').removeClass('active');
        $(this).closest('h3').addClass('active');
        var checkElement = $(this).next();
        if((checkElement.is('.oe_secondary_menu')) && (checkElement.is(':visible'))) {
            $(this).closest('h3').removeClass('active');
            checkElement.slideUp(400);
        }
        if((checkElement.is('.oe_secondary_menu')) && (!checkElement.is(':visible'))) {
            $('#cssmenu h3:visible').slideUp(400);
            checkElement.slideDown(400);
        }
    });

    $('.cssmenu > h3').hover(function () {
        if ($('.o_sub_menu.fix_icon_width').is(":visible")) {
            var leftpanel = $('.o_sub_menu.fix_icon_width').position().top;
            var menu = $(this).position().top;
            var total_top = leftpanel + menu + 40;
            $(this).next().addClass('iconic_menu');
            $(this).next('.iconic_menu.oe_secondary_menu').css({'top' : total_top + 'px'});
        }
    });

    $('.cssmenu .oe_menu_toggler').click(function(ev) {
        $('.cssmenu .oe_menu_toggler').removeClass('active');
        $(this).closest('.oe_menu_toggler').addClass('active');
        var checkElement = $(this).next();
        if((checkElement.is('.oe_secondary_submenu')) && (checkElement.is(':visible'))) {
            $(this).closest('.oe_menu_toggler').removeClass('active');
            checkElement.slideUp(400);
        }
        if((checkElement.is('.oe_secondary_submenu')) && (!checkElement.is(':visible'))) {
            $('#cssmenu .oe_menu_toggler:visible').slideUp(400);
            checkElement.slideDown(400);
        }
    });
    
    $('.o_sub_menu_content').find('.oe_menu_toggler').siblings('.oe_secondary_submenu').hide();
    
    $('.oe_secondary_submenu li a.oe_menu_leaf').click(function() {
        // Fix: active menu not reload again
        if ($(this).parent().hasClass('active')) {
            window.location.reload();
        } else {
            $('.oe_secondary_submenu li').removeClass('active');
            $(this).parent().addClass('active');
        }
        var $secondary_menu = $(this).closest('.oe_secondary_menu');
        if ($secondary_menu.hasClass('iconic_menu')) {
            $secondary_menu.removeClass('iconic_menu');
        }
    });
    
    // function display_clock_time(id) {
    //         var date = new Date();
    //         moment.locale(date_time_format_lang);
    //         var date_time = moment(date).format(date_time_format);

    //     $(".odoo_clock").text(date_time);
    //     setTimeout(function(){display_clock_time('.odoo_clock');}, 900);
    // }   
    // if ($('.odoo_clock').length >= 1){ display_clock_time('.odoo_clock'); }
    
    
    function switch_theme_views(iconic, is_mobile){
        var leftbar = $('div.o_sub_menu');
        if(iconic){
            if(is_mobile){
                leftbar.show();
            }
            leftbar.addClass('fix_icon_width');
            leftbar.find('.menu_heading').addClass('iconic_menu_heading');
            leftbar.find('.oe_secondary_menu').hide().addClass('iconic_menu');
            leftbar.find('.o_sub_menu_footer').hide();
        }else{
            if(is_mobile){
                leftbar.hide();
            }
            $('div.o_sub_menu.fix_icon_width').removeClass('fix_icon_width');
            leftbar.find('.menu_heading').removeClass('iconic_menu_heading');
            leftbar.find('.oe_secondary_menu').removeClass('iconic_menu');
            leftbar.find('.o_sub_menu_footer').show();
        }
        utils.set_cookie('theme_menu_style', JSON.stringify({
            'iconic_menu':iconic,
            'is_mobile':is_mobile,
        }), 2592000); // 30*24*60*60 = 2592000 = 30 days

    }

    // Detect Small Devices width
    var $window = $(window);
    function checkWidth() {
        var windowsize = $window.width();
        var leftbar = $('div.o_sub_menu');
        if (windowsize < 768) {
            leftbar.hide();
        } else {
            var side_menu = utils.get_cookie('side_menu');
            if(side_menu){
                var menu_style = JSON.parse(side_menu);
                if (menu_style.odooshoppe_menu == 'collapse'){
                    leftbar.addClass('fix_icon_width');
                    leftbar.find('.menu_heading').addClass('iconic_menu_heading');
                    leftbar.find('.oe_secondary_menu').hide().addClass('iconic_menu');
                    leftbar.find('.o_sub_menu_footer').hide();
                } else {
                    $('div.o_sub_menu.fix_icon_width').removeClass('fix_icon_width');
                    leftbar.find('.menu_heading').removeClass('iconic_menu_heading');
                    leftbar.find('.oe_secondary_menu').removeClass('iconic_menu');
                    leftbar.find('.o_sub_menu_footer').show();
                }
            }
            leftbar.show();
            // $('div.o_sub_menu.fix_icon_width').removeClass('fix_icon_width');
            // leftbar.find('.menu_heading').removeClass('iconic_menu_heading');
            // leftbar.find('.oe_secondary_menu').removeClass('iconic_menu');
            // leftbar.find('.o_sub_menu_footer').show();
        }
        if (windowsize > 991) {
            $('.o_control_panel ol.breadcrumb, .o_control_panel .o_cp_searchview, .o_control_panel .o_cp_left, .o_control_panel .o_cp_right').slideDown(500);
        }
    }
    checkWidth();
    $(window).resize(checkWidth);

    // Left sub menu spacing issues
    var isWindows = navigator.platform.toUpperCase().indexOf('WIN')!==-1;
    if (isWindows && $.browser.mozilla) {
        $('div.oe_secondary_menu.iconic_menu').css('margin-left', '-10px');
    }
    if (isWindows && /Edge/.test(navigator.userAgent)) {
        $('div.oe_secondary_menu.iconic_menu').css('margin-left', '-15px');
    }

});

});
