$(window).load(function() {

	function truncate(s, thresh) {
		return s.length > (thresh - 1) ? (s.substring(0, thresh) + " ...") : s
	}

	$(".dropdown-menu li a").click(function(e){
		console.log($(this).siblings(''));
		console.log($(this).find('.dropdown-toggle'));
		$(this).parents('.btn-group').find('.dropdown-toggle').html('<strong>' + 
		//$(this).parents('.dd-span').find('.dropdown-toggle').html('<strong>' + 
			truncate($(this).text(), 60)
			+ '</strong> <span class="caret"></span>'
		);
	});

	var substringMatcher = function(strs) {
		return function findMatches(q, cb) {
			console.log(q);
			var matches, substringRegex;
	 
			// an array that will be populated with substring matches
			matches = [];
	 
			// regex used to determine if a string contains the substring `q`
			substrRegex = new RegExp(q, 'i');
	 
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
		name: 'states',
		source: substringMatcher(restaurant_names)
	});

	$('.restaurant-names-typeahead').on('typeahead:selected', function(evt, item) {
		$('#restaurant-name-input').val(item);
	})

});