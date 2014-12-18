$(document).ready(function() {

	// light: switch on/off
	$(".btn-light-on, .btn-light-off").click(function() {
		$btn = $(this);
		$.post($btn.attr("action"), function(response) {
			if (response == "success") {
				$btn.closest(".btn-group").find(".btn").toggleClass("btn-primary").toggleClass("disabled");
			}
		});
	});

	// environment: update rooms
	$("#btn-environment-update").click(function() {
		// prevent double clicking
		$(this).remove();
		// reload with new data
		$.get($(this).attr("href"), function(response) {
			if (response === "success") {
				window.top.location=window.top.location;
			}
		});
		return false;
	});

});
