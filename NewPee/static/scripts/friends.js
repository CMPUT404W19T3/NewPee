
$(document).ready(function(){






    console.log("JS Working");


    var reject_button = document.querySelectorAll("#accept_Post_Button");
    var accept_button = document.querySelectorAll("#decline_Post_Button");
    var author_ids = document.querySelectorAll("#author_id");

    console.log(author_ids.length);
    console.log(reject_button);



    /*


    {
	"query":"friendrequest",
	"author": {
		"id":"http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
		"host":"http://127.0.0.1:5454/",
		"displayName":"Greg Johnson"
                "url":"http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
	},
	"friend": {
		"id":"http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e637281",
		"host":"http://127.0.0.1:5454/",
		"displayName":"Lara Croft",
                "url":"http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",

	}
}

*/



    for( var i = 0; i < (author_ids.length-1); i++){

    

    data = a;

    reject_button[i].addEventListener('click', event => {
        console.log("clicked");
        alert("yet");

        $.ajax({
            type: "POST",
            url: "api/author/<uuid:pk>/decline-friend-request/",
            contentType: 'application/json',
            headers:{"X-CSRFToken": csrftoken},
            data : data,
            success : function(json) {
                $("#request-access").hide();
                console.log("requested access complete");
                updateNumPostGet();
            },
            error: function (e) {
                console.log("ERROR: ", e);
            }
    
        });



    });


    accept_button[i].addEventListener('click', event => {

        alert("yet");

        data = {};
        author = {};
        friend = {};


        data["query"] = "friendrequest";
        data["author"] = author;
        data["friend"] = friend;

        $.ajax({
            type: "POST",
            url: "/api/friendrequest/",
            contentType: 'application/json',
            headers:{"X-CSRFToken": csrftoken},
            data : data,
            success : function(json) {
                $("#request-access").hide();
                console.log("requested access complete");
                updateNumPostGet();
            },
            error: function (e) {
                console.log("ERROR: ", e);
            }
    
        });

    });
    }






});