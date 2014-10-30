	$(document).ready(function() {
		console.log("ready")
		var date = new Date();
		var d = date.getDate();
		var m = date.getMonth();
		var y = date.getFullYear();
		
		var calendar = $('#calendar').fullCalendar({
			header: {
				left: 'prev,next today',
				center: 'title',
				right: ''
			},
			selectable: true,
			selectHelper: true,
			select: function(start, end, allDay) {
//				$('#myModal').modal()
				
				
				
				
				send_ajax(start.getDate(),start.getMonth()+1,start.getFullYear())
				/*				
				var title = prompt('Event Title:');
				if (title) {

					calendar.fullCalendar('renderEvent',
						{
							title: title,
							start: start,
							end: end,
							allDay: allDay
						},
						false // make the event "stick"
					);
					console.log(title)
				}
				calendar.fullCalendar('unselect');
				*/
			},
			editable: true,
			events: [
/*				{
					title: 'All Day Event',
					start: new Date(y, m, 1)
				},
*/			]
		});

		
		
	});

	send_ajax = function(date,month,year){
		$temp_var = getCookie("csrftoken")
		$.ajax({
			url:'/dashboard/',
			method:'POST',
			data:{"date":date,"month":month,"year":year,"csrfmiddlewaretoken":$temp_var},
			success:function(msg){

				$("#calender_order").html(msg)
				$("#myDayModal").modal()
				$temp_var = getCookie("csrftoken")
				$("input[name='csrfmiddlewaretoken']").val($temp_var)
			}
		})
	}
	
	function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $(document).on("submit",".cart_subforms_edit",function(event){
			
			event.preventDefault()
    		$id = $(this).prop("id")
    		$temp_terms = $id.split("__")
			$name = $temp_terms[1].split("_")[0]
			$course = $temp_terms[1].split("_")[1]
			$action = $temp_terms[1].split("_")[2]
			$(".cart_subforms_div").slideUp()
			$("#form__"+$name+"_"+$course).slideDown()
    		
    	})

    $(document).on("submit",".cart_subforms_remove",function(event){
			
			event.preventDefault()
    		$id = $(this).prop("id")
    		$temp_terms = $id.split("__")
			$name = $temp_terms[1].split("_")[0]
			$course = $temp_terms[1].split("_")[1]
			$action = $temp_terms[1].split("_")[2]
			var date = new Date();
			
			//$("input[name='date']").val(date.getDate())
			//$("input[name='month']").val(date.getMonth()+1)
			//$("input[name='year']").val(date.getFullYear())
			
			$(".cart_subforms_div").slideUp()
			$.ajax({
				url:'/remove_order/',
				method:'POST',
				data:$(this).serialize(),
				success:function(msg){
					console.log(msg)
					$("#calender_order").html(msg)		
				}
			})
			
    		
    	})

	$(document).on("submit",".cart_subforms",function(event){
			
			event.preventDefault()
			var date = new Date();
			
			//$("input[name='date']").val(date.getDate())
			//$("input[name='month']").val(date.getMonth()+1)
			//$("input[name='year']").val(date.getFullYear())
			$.ajax({
				url:'/edit_order/',
				method:'POST',
				data:$(this).serialize(),
				success:function(msg){
					$("#calender_order").html(msg)		
					
				}
			})
    		
    	})

	$(document).on("click","#close_subforms",function(event){
			
			$(".cart_subforms_div").slideUp()
    		
    	})