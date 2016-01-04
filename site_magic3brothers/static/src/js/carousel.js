 $(function(){
      // 初始化轮播
      $(".start-slide").click(function(){
         $("#myCarousel").carousel('cycle');
      });
      // 停止轮播
      $(".pause-slide").click(function(){
         $("#myCarousel").carousel('pause');
      });
      // 循环轮播到上一个项目
      $(".prev-slide").click(function(){
         $("#myCarousel").carousel('prev');
      });
      // 循环轮播到下一个项目
      $(".next-slide").click(function(){
         $("#myCarousel").carousel('next');
      });
      // 循环轮播到某个特定的帧 
      $(".slide-one").click(function(){
         $("#myCarousel").carousel(0);
      });
      $(".slide-two").click(function(){
         $("#myCarousel").carousel(1);
      });
      $(".slide-three").click(function(){
         $("#myCarousel").carousel(2);
      });
      // active about menu
      var url=window.location.href;
      if((url.indexOf('business') >= 0 || url.indexOf('culture')>= 0 || url.indexOf('news')>= 0 || url.indexOf('aboutus')>= 0) ){
         $("#top_menu li:eq(1)").attr("class","active");
      }else{
         $("#top_menu li:eq(1)").attr("class","");
      }

   });