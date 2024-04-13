$(function(){
	$.ajax({
		url: "http://web-01.salimjj03.tech/admin_home/",
                dataType: "html",
                success: function(data){
			$("#admin_home").html(data);
		}
	})

	$("#admin_dashbord").on("click", function() {
        	$.ajax({
        		url: "http://web-01.salimjj03.tech/admin_home/",
        		dataType: "html",
        		success: function(data){
				$("#admin_home").html(data);
			}
		})
	})
	$("#admin_transaction").on("click", function() {
		$.ajax({
                	url: "http://web-01.salimjj03.tech/admin_transactions",
                	dataType: "html",
                        success: function(data){
                        $("#admin_home").html(data);
			}
		})
        })
	$("#view_staff").on("click", function() {
                $.ajax({
                       url: "http://web-01.salimjj03.tech/admin_users",
                       dataType: "html",
                       success: function(data){
			       $("#admin_home").html(data);
		       }
		})
	})
	$("#add_staff").on("click", function() {
		$.ajax({
			url: "http://web-01.salimjj03.tech/register",
			dataType: "html",
			success: function(data){
				$("#admin_home").html(data);
			}
		})
	})
	$("#logout").on("click", function(){
		window.location.href = 'http://web-01.salimjj03.tech/logout';
	})
	$("#pass").on("click", function(){
                var id = $("#pass").data("pass")
                var value = prompt("select new password")
		if (value === null) {
			return
		}
                var dic = JSON.stringify({password: value})
                $.ajax({
                        url: "http://web-01.salimjj03.tech/user/" + id,
                        method: "PUT",
                        data: dic,
                        contentType: "application/json",
                        success: function(res) {
                                alert(res)
                        }
                })
        })
})
