$(window).load(function() {

	function truncate(s, thresh) {
		return s.length > (thresh - 1) ? (s.substring(0, thresh) + " ...") : s
	}

	$(".dropdown-menu li a").click(function(){
		$(this).parents('.btn-group').find('.dropdown-toggle').html('<strong>' + 
			truncate($(this).text(), 60)
			+ '</strong> <span class="caret"></span>'
		);
	});
/*
	$( document.body ).on( 'click', '.dropdown-menu li', function( event ) {
	
	   var $target = $( event.currentTarget );
	 
		$target.closest( '.btn-group' )
			.find( '[data-bind="label"]' ).text( $target.text() )
				.end()
			.children( '.dropdown-toggle' ).dropdown( 'toggle' );
		return false;
	
	});
*/

});