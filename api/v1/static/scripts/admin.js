$(function(){
	$.ajax({
		url: "http://localhost:5000/admin_home/",
                dataType: "html",
                success: function(data){
			$("#admin_home").html(data);
		}
	})

	$("#admin_dashbord").on("click", function() {
        	$.ajax({
        		url: "http://localhost:5000/admin_home/",
        		dataType: "html",
        		success: function(data){
				$("#admin_home").html(data);
			}
		})
	})
	$("#admin_transaction").on("click", function() {
		$.ajax({
                	url: "http://localhost:5000/admin_transactions",
                	dataType: "html",
                        success: function(data){
                        $("#admin_home").html(data);
			}
		})
        })
	$("#view_staff").on("click", function() {
                $.ajax({
                       url: "http://localhost:5000/admin_users",
                       dataType: "html",
                       success: function(data){
			       $("#admin_home").html(data);
		       }
		})
	})
	$("#add_staff").on("click", function() {
		$.ajax({
			url: "http://localhost:5000/register",
			dataType: "html",
			success: function(data){
				$("#admin_home").html(data);
			}
		})
	})
	$("#logout").on("click", function(){
		window.location.href = 'http://localhost:5000/logout';
	})
	$("#pass").on("click", function(){
                var id = $("#pass").data("pass")
                var value = prompt("select new password")
		if (value === null) {
			return
		}
                var dic = JSON.stringify({password: value})
                $.ajax({
                        url: "http://localhost:5000/user/" + id,
                        method: "PUT",
                        data: dic,
                        contentType: "application/json",
                        success: function(res) {
                                alert(res)
                        }
                })
        })
})
