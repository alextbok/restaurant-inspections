$(window).load(function() {

	$('.close').click(function() {

		$('#results-alert').hide();

	})
	$(".update-btn").click(function() {
		return update(null);
	});

	function truncate(s, thresh) {
		return s.length > (thresh - 1) ? (s.substring(0, thresh) + " ...") : s;
	}

	$(".dropdown-menu li a").click(function(e){
		$(this).parents('.btn-group').find('.dropdown-toggle').html('<strong>' + 
			truncate($(this).text(), 60)
			+ '</strong> <span class="caret"></span>'
		);
	});

	var substringMatcher = function(strs) {
		return function findMatches(q, cb) {

			var matches = [];
			var substrRegex = new RegExp(q, 'i');
	 
			// iterate through the pool of strings and for any string that
			// contains the substring `q`, add it to the `matches` array
			$.each(strs, function(i, str) {
				if (substrRegex.test(str)) {
					matches.push(str);
				}
			});
			cb(matches);
		};
	};

	$('.restaurant-names-typeahead').typeahead({
		hint: true,
		highlight: true,
		minLength: 1
	},
	{
		source: substringMatcher(restaurant_names)
	});

	$('.restaurant-names-typeahead').on('typeahead:selected', function(evt, item) {
		$('#restaurant-name-input').val(item);
	});

	$('.restaurant-names-typeahead').on('keydown', function (e) {
		if ($('.restaurant-names-typeahead').val() == '') {
			$('#restaurant-name-input').val('');
		}
	});

});

