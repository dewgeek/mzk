
$(document).ready(function(){

	$update_totalcost()

	$("input:checkbox").change(function(){
		$update_totalcost()		
	})

	$("select").change(function(){
		$update_totalcost()
		$update_subcost($(this).prop("name"), $(this).val())			
	})	

	$("#submit_form").click(function(){
		$submit = false
		for(i=0;i<$coursesArray.length;i++){
			if($("#check_"+ $coursesArray[i]).prop("checked")){
				$submit = true
			}
		}
		if($submit){
			$.ajax({
				type: "POST",
				url: "/orders/",
				data: $("#order_form").serialize(),
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
		}else{
			alert("Check something")
		}
	})

	$(".slideshow").cycle()

	$(document).on("submit", '.cartform', function(event) { 
		$("input[name='csrfmiddlewaretoken']").val()
		//$(this).html('')
	    event.preventDefault()
		$td_id = $(this).prop("id").split('__')[1]
	    $.ajax({
				type: "POST",
				url: "/delete_order/",
				data: $(this).serialize(),
				beforeSend:function(){

				},
				success: function(msg){

					$('#'+$td_id).remove()
				},
				error: function(msg){
					console.log(msg)
				},
			})
	});

	

})

//Defining Courses Array (Need to be changed, if there is a change in Courses)
$coursesArray = ['BreakFast','Lunch','Dinner']

$update_totalcost = function(){

	//Initializing the Cost
	$value = 0

	$strs = $("#order_form").serializeArray()
	$.each($strs, function(i, fd) {
	    if($.inArray(fd.name,$coursesArray) != -1){
	    	$temp_price = $("#order_form input[name='price_"+fd.name+"']").val()
	    	$temp_span = $("#order_form select[name='span_"+fd.name+"']").val()
	  		$value = $value + $temp_price*$temp_span
	    }
	});
	
	$("#total_cost").html("<p>"+$value+"</p>")
}

$update_subcost = function(name,span){
	$course = name.split('_')[1]
	$temp_price = $("#order_form input[name='price_"+$course+"']").val()
	$("#subcost_"+ $course ).html(span*$temp_price)
}



