$(function() {
	$.ajax({
                url: "http://localhost:5000/user_home/",
                dataTyle: "html",
                success: function(data) {
                                $("#page").html(data);
                        }
        })

	$("#dashbord").on("click", function(){
                $.ajax({
                        url: "http://localhost:5000/user_home/",
                        dataType: "html",
                        success: function(data) {
                                $('#page').html(data);
                        },
                        error: function(xhr, status, error) {
                                console.error("Error loading file:", error);
 				}
                })
        })

	$("#add_nav").on("click", function(){
                $.ajax({
                        url: "http://localhost:5000/add_record/",
                        dataType: "html",
                        success: function(data) {
                                $('#page').html(data);
                        },
                        error: function(xhr, status, error) {
                                console.error("Error loading file:", error);
 				}
                })
        })
	$("#transaction").on("click", function(){
                $.ajax({
                        url: "http://localhost:5000/transections/",
                        dataType: "html",
                        success: function(data) {
                                $('#page').html(data);
                        },
                        error: function(xhr, status, error) {
                                console.error("Error loading file:", error);
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
