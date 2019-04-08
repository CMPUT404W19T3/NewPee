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
var post_url = location.pathname;
var post_uuid = post_url.split("/")[2];
console.log(post_uuid)
$(document).ready(function(){

    const elementMakeComment = document.getElementById("comment_creation_submit");
    var userID = document.getElementById("userID").value;
    var userUUID = userID.split("/")[5];
    var user_api_url = "/api/authors/" + userID;
    const deletePostButton = document.querySelector("#remove_post_submit");
    var author;
   

    deletePostButton.addEventListener('click', event =>{
        //event.preventDefault();
        console.log(userUUID);
        console.log(userID);
        console.log("DELETING");
        $.ajax({
            method: "GET", // type --> method, the HTTP method used for the request.
            url: userID, // URL to which the request is sent.
            contentType: 'application/json', // The MIME type being sent to the server.
            headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
            success : function(json) {  // This function is called if the request is successful. Data is returned from the server.
                author = json;
                console.log(author.posts_created);
                var data = {};
                data["posts_created"] = author.posts_created - 1;
                console.log(JSON.stringify(data));

                $.ajax({
                    method: "PATCH", // type --> method, the HTTP method used for the request.
                    url: userID, // URL to which the request is sent.
                    contentType: 'application/json', // The MIME type being sent to the server.
                    headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
                    data: JSON.stringify(data),  // Data to be sent to the server. Transoformed to query string if not one yet.
                    success : function(json) {
                        console.log(json);
                        $("#request-access").hide();
                    },  // This function is called if the request is successful. Data is returned from the server.
                    error: function (e) {
                        console.log("ERROR: ", e);
                    } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
                });
                $("#request-access").hide();
            },
            error: function (e) {
                console.log("ERROR: ", e);
            } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
        });
        $.ajax({
            method: "DElETE", // type --> method, the HTTP method used for the request.
            async: false, // Synchronous request.
            url: "/api/posts/"+post_uuid, // URL to which the request is sent.
            contentType: 'application/json', // The MIME type being sent to the server.
            headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
            success : function(json) {
                $("#request-access").hide();
                console.log("requested access complete");
            }, // This function is called if the request is successful. Data is returned from the server.
            error: function (e) {
                console.log("ERROR: ", e);
            } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
        });
        //location.pathname = "/authors/" + userUUID;
    });
    elementMakeComment.addEventListener('submit', event => {
        //event.preventDefault();
        // https://stackoverflow.com/questions/31878960/calling-django-view-from-ajax
        var postID = location.pathname.split("/")[2];
        var comment = document.querySelector("#comment").value;
        var data = JSON.stringify({
            parent: postID,
            author : userID,
            content: comment,
            csrfmidddlewaretoken: csrftoken,
        });
        console.log(data);
        // Goes to post_created
        // author.view post_created view
        $.ajax({
            method: "POST", // type --> method, the HTTP method used for the request.
            async: false, // Synchronous request.
            url: "/api/comments", // URL to which the request is sent.
            contentType: 'application/json', // The MIME type being sent to the server.
            headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
            data : data, // data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
            success : function(json) {
                $("#request-access").hide();
                console.log("requested access complete");
            }, // This function is called if the request is successful. Data is returned from the server.
            error: function (e) {
                console.log("ERROR: ", e);
            } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
        });
    });
});