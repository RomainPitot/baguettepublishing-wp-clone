(function($) {
	"use strict";
	$(window).on("load", function() {
		// makes sure the whole site is loaded
		//preloader
		$("#status")
			.delay(550)
			.fadeOut(); // will first fade out the loading animation
		$("#preloader")
			.delay(1050)
			.slideUp("slow"); // will fade out the white DIV that covers the website.
	});
})(jQuery);
