/*
   
    Template Name : Wesoon - Creative Coming Soon
    Author : UiPasta Team
    Website : http://www.uipasta.com/
    Support : http://www.uipasta.com/support/
	
	
*/



/*
   
   Table Of Content
   
   1. Preloader
   2. Scroll To Top
   3. CountDown Timer
   4. Ajaxchimp for Subscribe Form
   5. Video and Google Map Popup
   6. Detail Box ( Slider by Owl Carousel )
   7. Owl Carousel Navigation
 

*/


(function ($) {
    'use strict';

    jQuery(document).ready(function () {

        
       /* Preloader */
		
        $(window).load(function () {
            $('.preloader').delay(800).fadeOut('slow');
        });
		
		
       
       /* Scroll To Top */
		
        $(window).scroll(function(){
        if ($(this).scrollTop() >= 700) {
            $('.scroll-to-top').fadeIn();
         } else {
            $('.scroll-to-top').fadeOut();
         }
	   });
	
	
        $('.scroll-to-top').click(function(){
          $('html, body').animate({scrollTop : 0},800);
          return false;
         });
		
       
	   
       /* CountDown Timer */	
	   	
        $('.countdown').downCount({
            date: '11/14/2018 15:00:00',   // Change the launch date from here
            offset: +5.5
          }, function () {
             alert('Countdown Done, We are just going to launch our website!');
        });


		
        /* Ajaxchimp for Subscribe Form */
		
        $('#mc-form').ajaxChimp();
		 
		 
		 
        /* Video and Google Map Popup */
		 
        $('.video-popup, .map-popup').magnificPopup({
          disableOn: 700,
          type: 'iframe',
          removalDelay: 160,
          preloader: false,
          fixedContentPos: false
        });
		 
	   
		 
        /* Detail Box ( Slider by Owl Carousel ) */

        $(".detail-box").owlCarousel({
            items: 1,
            autoPlay: false,
            stopOnHover: false,
            itemsDesktop: [1199, 1],
            itemsDesktopSmall: [980, 1],
            itemsTablet: [768, 1],
            itemsTabletSmall: false,
            itemsMobile: [479, 1],
            autoHeight : true,
            pagination: false,
            transitionStyle : "fadeUp"
        });
		

        /* Owl Carousel Navigation */
		
        $(document).ready(function() {
          var owl = $("#detail-box-carousel");
          owl.owlCarousel();
            $(".next").click(function(){
            owl.trigger('owl.next');
        })
            $(".prev").click(function(){
            owl.trigger('owl.prev');
        })
        });
		       
		   
        });

   })(jQuery);