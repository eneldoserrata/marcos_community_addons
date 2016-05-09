//jQuery to collapse the navbar on scroll
$(document).ready(function(){
    $(window).scroll(function() {
        if ($(".navbar").offset().top > 50) {
            $(".navbar-fixed-top").addClass("top-nav-collapse");
        } else {
            $(".navbar-fixed-top").removeClass("top-nav-collapse");
        }
    });
});

//jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        /*event.preventDefault();*/
    });
});

    $(document).ready(function()
   {
      var number_li=($("#top_menu li").size());
      if (number_li<18)
      {
        $('#more_menu').hide();
      }
      else
      {
        $('#theme_about').hide();
        $('#theme_service').hide();
        $('#theme_projects').hide();
        $('#theme_testimonials').hide();
        $('#more_menu').show();
      }
      $('#theme_about').click(function(){
        $("#top_menu li").first().removeClass( "active" );
        $("#top_menu li").removeClass( "active" );
        $('#theme_about').addClass('active');
     });
      $('#theme_service').click(function(){
        $("#top_menu li").removeClass( "active" );
        $('#theme_service').addClass('active');
     });
     $('#theme_projects').click(function(){
        $("#top_menu li").removeClass( "active" );
        $('#theme_projects').addClass('active');
     });
     $('#theme_testimonials').click(function(){
        $("#top_menu li").removeClass( "active" );
        $('#theme_testimonials').addClass('active');
     });

     $("#theme_about").click(function () {
            window.location.href = "/#about-us";
        });
     $("#theme_service").click(function () {
            window.location.href = "/#service";
        });
     $("#theme_projects").click(function () {
            window.location.href = "/#our-projects";
        });
     $("#theme_testimonials").click(function () {
            window.location.href = "/#testimonials";
        });
    
    if($("#theme_about").prev().index()>4)
    {
    	$("#theme_testi").append($("#top_menu li:nth-child(5)").nextUntil($("#more_menu").prev()));
    }
});
  // animation effect js
var $animation_elements = $('.animation-element');
var $window = $(window);

function check_if_in_view() {
  var window_height = $window.height();
  var window_top_position = $window.scrollTop();
  var window_bottom_position = (window_top_position + window_height);
 
  $.each($animation_elements, function() {
    var $element = $(this);
    var element_height = $element.outerHeight();
    var element_top_position = $element.offset().top;
    var element_bottom_position = (element_top_position + element_height);
 
    //check to see if this current container is within viewport
    if ((element_bottom_position >= window_top_position) &&
        (element_top_position <= window_bottom_position)) {
      $element.addClass('in-view');
    } else {
      $element.removeClass('in-view');
    }
  });
}
$window.on('scroll resize', check_if_in_view);
$window.trigger('scroll');


