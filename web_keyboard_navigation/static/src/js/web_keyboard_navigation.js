//////////////////////////////////////////////////////////////////////////////
//    OpenERP, Open Source Management Solution    
//    Copyright (c) 2010-2012 Elico Corp. All Rights Reserved.
//
//    Author: Yannick Gouin <yannick.gouin@elico-corp.com>
//            Jerome Sonnet <jerome.sonnet@be-cloud.be> port to 9.0
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
/////////////////////////////////////////////////////////////////////////////:

$.ctrl = function(key, callback, args) {
    $(document).keydown(function(e) {
        if(!args) args=[]; // IE barks when args is null 
        if((e.keyCode == key.charCodeAt(0) || e.keyCode == key) && e.ctrlKey) {
            callback.apply(this, args);
            return false;
        }
    });        
};

//Edit the current object
$.ctrl('E', function() {
	$('.oe_form_button_edit').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//Save the current object
$.ctrl('S', function() {
	$('.oe_form_button_save').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//Cancel the current object edition
$.ctrl('Z', function() {
	$('.oe_form_button_cancel').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//Delete the current object
/*$.ctrl('46', function() {
	$('.oe_form_button_delete').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});*/

//New object
$.ctrl('N', function() {
	$('.oe_form_button_create').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
	$('.oe_list_add').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//Duplicate the current object
/*$.ctrl('D', function() {
	$('.oe_form_button_duplicate').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});*/

//Previous object
$.ctrl('38', function() {
	$('.oe-pager-button[data-pager-action="previous"]').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//Next object
$.ctrl('40', function() {
	$('.oe-pager-button[data-pager-action="next"]').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//Last object
/*$.ctrl('34', function() {
	$('.oe_button_pager[data-pager-action="last"]').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});*/