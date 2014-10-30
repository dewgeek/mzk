
$call_cart = function(){
	
	$.ajax({
				type: "POST",
				url: "/list_orders/",
				data: {"csrfmiddlewaretoken":getCookie("csrftoken")},
				beforeSend:function(){
					$("#myModal").modal()
					$("#cart tbody").html("<img src='/static/images/ajax-loader.gif'/>")
				},
				success: function(msg){
					
					$("#cart tbody").html(msg)
				},
				error:function(msg){
					$("#cart tbody").html("there is an error , please retry after sometime")	
				}
			})
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

$toggle_pswd_form = function(){

	console.log($("#pswd_form_div").attr("display"))

}