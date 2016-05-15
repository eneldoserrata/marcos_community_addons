
$(document).ready(function (require) {
onload_hide_wishlise_icon();

odoo.define('website_sale.cart', function (require) {
"use strict";
var ajax = require('web.ajax');

$('.oe_website_sale').each(function () {
    var $oe_website_sale = this;


$($oe_website_sale).on("change", ".oe_cart input.js_quantity", function (ev) {
        ev.preventDefault();
        var $input = $(this);
        var value = parseInt($input.val(), 10);
        var line_id = parseInt($input.data('line-id'),10);
        if (isNaN(value)) value = 0;
        ajax.jsonRpc("/shop/cart/update_json", 'call', {
            'line_id': line_id,
            'product_id': parseInt($input.data('product-id'),10),
            'set_qty': value})
            .then(function (data) {
                if (!data.quantity) {
                    window.location.href = document.URL;
                    return;
                }
                var $q = $(".my_cart_quantity");
                $q.parent().parent().removeClass("hidden", !data.quantity);
                $q.html(data.cart_quantity).hide().fadeIn(600);

                $input.val(data.quantity);
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
                $("#cart_total").replaceWith(data['website_sale.total']);
                return false;
            });
            return false;
    });
});
});
});


function check_for_variant(product_id) {
/* FUNCTION TO ADD PRODUCT VARIANT PRODUCT IN WISHLIST */
    $.ajax({
	url : "/shop/check_for_variant/product_id", 
		data: { product_id: product_id},
	success : function(data) {
		var d = $.parseJSON(data);
		if(d.message){
	           //$("#link_for_variant").val(true);
						 //$("#return_p_id").val(product_id);
						 $("#wishlist_icon").hide();
						 $("#add_to_wishlist").hide();
		}
		else{
		   //$("#link_for_variant").val(false);
		   //$("#return_p_id").val(product_id);
		   $("#wishlist_icon").show();
		   $("#add_to_wishlist").show();
		}
	},
	error : function() {
		
	}
    });
}


/*LOAD THIS FUNCITON ON LOAD OF /shop/product/ PAGE TO HIDE ADD TO WISHLIST ICON*/
function onload_hide_wishlise_icon() {
	var url = window.location.href;
	//alert(window.location.href);
	if(url.indexOf('/shop/product/') != -1){
	    //console.log("create post is working!");
		var product_id = document.getElementById("wishlist_product_id").value;
		//alert(product_id);
		if (product_id){
			check_for_variant(product_id);
		}
	}
	};



function add_product_to_wishlist() {
    /* TO ADD PRODUCT IN WISHLIST */
    var product_id = document.getElementsByName("product_id")[0].value;
		//alert(product_id);
    $.ajax({
        url : "/shop/add_product_to_wishlist", 
		data: { product_id: product_id},
        success : function(data) {
		check_for_variant(product_id);
		//location.reload();
        },
        error : function() {
        }
    });
};

function remove_product_from_wishlist(ele) {
	/* TO DELETE PRODUCT FROM WISHLIST VIEW */
    var tab_parent = ele.parentElement.parentElement.parentElement;
    var tr_parent = ele.parentElement.parentElement;
    var product_id = ele.parentElement.childNodes[1].value;
    tab_parent.removeChild(tr_parent);
    $.ajax({
        url : "/shop/remove_product_from_wishlist/product_id", 
		data: { product_id: product_id},
        success : function(data) {
        	location.reload();
        	//window.location.href = document.URL;
        },
        error : function() {
        }
    });
     return false;
};


function remove_product_from_wishlist_from_cart(ele) {
	/* TO DELETE PRODUCT FROM PRODUCT LIST */
   var products = ele.parentElement.childNodes;
   var product_id = '';
   for (var i = 0; i < products.length; i++) {
        if (products[i].name == "product_id") {
            product_id = products[i].value;
         }
    }
    if(!product_id){
    	alert("We did not get product id");
    	return false;
    }
    $.ajax({
        url : "/shop/remove_product_from_wishlist/product_id", 
		data: { product_id: product_id},
        success : function(data) {
        	location.reload();
        },
        error : function() {
        }
    });
};



function view_my_wishlist() {
	/* TO VIEW PRODUCT IN WISHLIST*/
    var product_id = document.getElementsByName("product_id")[0].value;
    $.ajax({
        url : "shop/view_my_wishlist", 
		data: { product_id: product_id},
        success : function() {
        },
    });
};

function add_product_to_wishlist_from_cart(ele) {
    var tab_parent = ele.parentElement.parentElement.parentElement;
    var tr_parent = ele.parentElement.parentElement;
    var products = ele.parentElement.childNodes;
    var product_id = '';
    for (var i = 0; i < products.length; i++) {
        if (products[i].name == "product_id") {
            product_id = products[i].value;
         }
    }
    if(!product_id){
    	alert("We did not get product id");
    	return false;
    }
    $.ajax({
        url : "/shop/add_product_to_wishlist_from_cart/product_id", 
		data: { product_id: product_id},
        success : function() {
        	//location.reload('/shop/cart/');
                location.replace('/shop/cart/')
        },
        error : function() {
        }
    });
};

function add_product_to_wishlist_from_shop(ele) {
    var tab_parent = ele.parentElement.parentElement.parentElement;
    var tr_parent = ele.parentElement.parentElement;
    var products = ele.parentElement.childNodes;
    var product_id = '';
    for (var i = 0; i < products.length; i++) {
        if (products[i].name == "product_id") {
            product_id = products[i].value;
         }
    }
    if(!product_id){
    	alert("We did not get product id");
    	return false;
    }
    $.ajax({
        url : "/shop/add_product_to_wishlist_from_shop/product_id", 
		data: { product_id: product_id},
        success : function() {
        	location.reload();
        },
        error : function() {
        }
    });
};

/* TO MOVE PRODUCT TO MY CART FROM WISHLIST */
function move_product_to_cart(ele) {
		//alert('move to cart');
    var tab_parent = ele.parentElement.parentElement.parentElement;
    var tr_parent = ele.parentElement.parentElement;
    var product_id = ele.parentElement.childNodes[1].value;
    tab_parent.removeChild(tr_parent);
    //alert(product_id);
    $.ajax({
        url : "/shop/move_product_to_cart/product_id", 
				data: {product_id: product_id},
        success : function(data) {
					//var d = $.parseJSON(data);
					//alert('success');
        	//alert(data);
					//$("#hide_wshlist_poriduct").hide();
        	//location.reload();
        	window.location.href = document.URL;
        },
        error : function() {
					//location.reload();
					//alert(document.URL);
					//alert('error');
					//location.reload();
					window.location.href = document.URL;
        }
    });
     return false;
};


