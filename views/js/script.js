/* Author:

*/


/* Shows notifications for 10 secs if no timeout is given */

function showNotification(thetitle, thecontent, mytimeout) {

	if (isNaN(parseInt(mytimeout))) {
		mytimeout = 10000;
	}

	$.notification( 
		{
			title: thetitle,
			content: thecontent,
			timeout: mytimeout,
			showTime: true,
			border: true,
		}
	);
}

function errorNotification(thetitle, thecontent, mytimeout) {

	if (isNaN(parseInt(mytimeout))) {
		mytimeout = 10000;
	}

	$.notification( 
		{
			title: thetitle,
			content: thecontent,
			timeout: mytimeout,
			showTime: true,
			border: true,
			error: true,
		}
	);
}

function successNotification(thetitle, thecontent, mytimeout) {

	if (isNaN(parseInt(mytimeout))) {
		mytimeout = 10000;
	}
	
	$.notification( 
		{
			title: thetitle,
			content: thecontent,
			timeout: mytimeout,
			showTime: true,
			border: true,
			success: true,
		}
	);
}


//check ui for notificaions every 3 seconds...

function getNotifications(){
	
	$.getJSON("/ui", function(data) {
		$.each(data, function (name, data) {
			if (data.type == "error") {
				errorNotification(data.title, data.message)
			} else if (data.type == "success") {
				successNotification(data.title, data.message)
			} else {
				showNotification(data.title, data.message)
			}
			//console.log(this.message)
		});
	})
}

function addNotification(type, title, message) {

	args = {
		'type': type,
		'title': title,
		'message': message
	}

	$.post("/ui/addNotification", args, function(data){
		console.log(data)
	})

}

//notifications only for active window...
var myVar = setInterval(function(){getNotifications()},3000);

$(window).focus(function(){
	myVar = setInterval(function(){getNotifications()},3000);
  console.log(myVar)
});
$(window).blur(function(){
	console.log(myVar)
  console.log(clearInterval(myVar))
});
