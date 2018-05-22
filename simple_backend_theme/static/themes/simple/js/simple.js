$( document ).ready(function() {
  
    // --- slider for the leftside menu -->
    $("#slider_strip").on('click', function(){
      
      if( $(this).find('.fa').hasClass('fa-arrow-left') ){
        $(".o_sub_menu").animate({
          margin: '0 0 0 -200px',
        }, 300, function(){
            $(this).find('.fa')
              .removeClass('fa-arrow-left')
              .addClass('fa-arrow-right')
        })
      } else {
        $(".o_sub_menu").animate({
          margin: '0 0 0 0px',
        }, 300, function(){
            $(this).find('.fa')
              .removeClass('fa-arrow-right')
              .addClass('fa-arrow-left')
        })                          
      }
    })
    // --- /slider for the leftside menu -->
  
    // --- slider for the footer -->
    $("#slider_footer").on('click', function(){
      
      if( $(this).find('.fa').hasClass('fa-arrow-down') ){
        $("footer").animate({
          margin: '0 0 -90px 0',
        }, 300, function(){
            $(this).find('.fa')
              .removeClass('fa-arrow-down')
              .addClass('fa-arrow-up')
        })
      } else {
        $("footer").animate({
          margin: '0 0 0px 0',
        }, 300, function(){
            $(this).find('.fa')
              .removeClass('fa-arrow-up')
              .addClass('fa-arrow-down')
        })                          
      }
    })
    // --- /slider for the footer -->
  
    // --- worldtime portlet -------------------
    if ($("#worldtime") != null) {
      
      // --- display current time -------------
      current_time = function() {
        var d, data, hour, minute, second;
        d = new Date();
        second = d.getSeconds();
        minute = d.getMinutes();
        hour = d.getHours();
        return hour + ":" + minute + ":" +  second
      }

      setInterval(function() {
        var ct;
        ct = current_time()
        $("#worldtime").html(ct)
      }, 1000);
      // --- /display current time -------------
      
    } 
    // --- worldtime portlet -------------------
});
