  $(document).ready(function() {
    function checkWidth() {
      var windowsize = $(window).width();
      var leftbar = $('div.o_sub_menu');
      if(windowsize < 768){
        leftbar.show();
      }
    }
    checkWidth();
    $(window).resize(checkWidth);
    $('.oe_secondary_submenu li a.oe_menu_leaf').click(function() {
      $('#odooMenuBarNav').toggleClass('in');
    });
  });
