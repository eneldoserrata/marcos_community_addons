console.log("ge loaded");

var showing = true;
$(function(){
    $(".ge_toggle_button").click(function(){
        console.log("Clicked");

        if(showing){
            $(".o_sub_menu").css("margin-left", "-220px");
        } else {
            $(".o_sub_menu").css("margin-left", "0px");
        }

        showing = !showing;

    });
});
