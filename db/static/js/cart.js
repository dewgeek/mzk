
$(document).ready(function(){
	$("form").validate()
	
	$("#cartButton").click(function(){
		$call_cart("/list_orders/")
	})
	
})



$("form input:checkbox").click(function(){
	change_form($(this).prop("value"),$(this).prop("name").split("_")[0],$(this).prop("checked"))
})

function change_form(main_val,temp_val,status){
	form_elems = ["name","landmark","mobile"]
	for(i=0;i<form_elems.length;i++){
		$("input[name="+"'"+temp_val+"_"+form_elems[i]+"']").prop("readonly",status)
	}
	$("textarea[name="+"'"+temp_val+"_address']").prop("readonly",status);

	if(status){
		for(i=0;i<form_elems.length;i++){
			$("input[name="+"'"+temp_val+"_"+form_elems[i]+"']").val($("input[name="+"'"+main_val+"_"+form_elems[i]+"']").val())
		}
		$("textarea[name="+"'"+temp_val+"_address']").val($("textarea[name="+"'"+main_val+"_address']").val());
	}
}

