function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
$(document).ready(function(){
    console.log("JS Working");
    var reject_button = document.querySelectorAll("#decline_Post_Button");
    var accept_button = document.querySelectorAll("#accept_Post_Button");
    var author_ids = document.querySelectorAll("#author_id");
    //var allButtonsOnPage = document.querySelectorAll('button');
    var logButtonIndex = function(buttonIndex) {
        console.log('buttonIndex:', buttonIndex);
      }
    console.log(author_ids);
    console.log(reject_button);
    console.log(author_ids[0])
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
    var imageArray = new Array();
    for( var i = 0; i <= (author_ids.length); i++){
        imageArray[i] = accept_button[i];
    }
    console.log(imageArray)
    function sendRequest(i){
        data = {};
        author = {};
        friend = {};
        author["id"] = user_id;
        author["host"] = user_host;
        author["displayName"] = user_displayName;
        author["user_url"] = user_url;
        console.log(  i );
        friend["id"] = author_ids[i].innerHTML;
        console.log(friend)
        data["query"] = "friendrequest";
        data["type"] = "local_add";
        data["author"] = author;
        data["friend"] = friend;
        $.ajax({
            type: "POST",
            url: "/api/friendrequest",
            contentType: 'application/json',
            headers:{"X-CSRFToken": csrftoken},
            data: JSON.stringify(data),
            success : function(json) {
                $("#request-access").hide();
                console.log("requested access complete");
            },
            error: function (e) {
                console.log("ERROR: ", e);
            }
        });
    }

    function declineRequest(i){
        data = {};
        author = {};
        friend = {};
        author["id"] = user_id;
        author["host"] = user_host;
        author["displayName"] = user_displayName;
        author["user_url"] = user_url;
        friend["id"] = author_ids[i].innerHTML;
        console.log(friend)
        data["query"] = "declinerequest";
        data["type"] = "local_add";
        data["author"] = author;
        data["friend"] = friend;
        $.ajax({
            type: "POST",
            url: "/api/friendrequest",
            contentType: 'application/json',
            headers:{"X-CSRFToken": csrftoken},
            data: JSON.stringify(data),
            success : function(json) {
                $("#request-access").hide();
                console.log("requested access complete");
            },
            error: function (e) {
                console.log("ERROR: ", e);
            }
        });
    }

    // LOOP Through our accept buttons
    for (let j = 0; j < accept_button.length; j++) {
        let button = accept_button[j];
        button.addEventListener('click', function() {
            logButtonIndex(j);
            sendRequest(j);
        });
    }
      for (let j = 0; j < reject_button.length; j++) {
        let button = reject_button[j];
        button.addEventListener('click', function() {
            logButtonIndex(j);
            declineRequest(j);
        });
      }

    /*
    reject_button[i].addEventListener('click', event => {
        value = i;
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
    });
    }
    i = 0;
    */
});