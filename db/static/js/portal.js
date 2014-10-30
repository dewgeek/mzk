$(document).ready(function(){

	$("form").submit(function(e){
		d = $(this).prop('name')
		console.log(d)

		e.preventDefault()
				
		$.ajax({
			url:$(this).prop('action'),
			method:'POST',
			data:$(this).serialize(),
			success:function(msg){
				reply = $.parseJSON(msg)
				if(reply["status"]=="Success"){
					window.location = '/cart/'
				}
				else{
					switch(d){
						case "loginForm":
							$("#id_username_1_error").html("");
							$("#id_password_1_error").html("");
							$("#form_error").html("");

							if("username" in reply["message"]){
								$("#id_username_1_error").html(reply["message"]["username"][0]);
							}
							if("password" in reply["message"]){
								$("#id_password_1_error").html(reply["message"]["password"][0]);
							}
							if("default" in reply["message"]){
								$("#form_error").html(reply["message"]);
							}
						case "registerForm":	

							$("#id_username_2_error").html("");
							$("#id_password_2_error").html("");
							$("#id_pswd_error").html("");
							$("#id_email_error").html("");
							$("#reg_form_error").html(reply["message"]);

							if("username" in reply["message"]){
								$("#id_username_2_error").html(reply["message"]["username"][0]);
							}
							if("password" in reply["message"]){
								$("#id_password_2_error").html(reply["message"]["password"][0]);
							}
							if("pswd" in reply["message"]){
								$("#id_pswd_error").html(reply["message"]["password"][0]);
							}
							if("email" in reply["message"]){
								$("#id_email_error").html(reply["message"]["email"][0]);
							}
							if("default" in reply["message"]){
								$("#reg_form_error").html(reply["message"]);
							}
						}
						
				}
			}
		})
	})
	
})
