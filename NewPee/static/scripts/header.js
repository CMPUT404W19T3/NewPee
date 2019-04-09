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

$(document).ready(function(){
    var user_id = document.getElementById("userIDSpan").innerHTML;
    //var user_id = document.getElementById("userID").value; // grabbing from hidden value through django context
    var user_id_spliced = user_id.split("/");
    var user_api_url = "/api/authors/" + user_id_spliced[user_id_spliced.length-1];
    var friend_api_url =   "/api/author/"+ user_id_spliced[user_id_spliced.length-1] +  "/friendrequest"

    function grabFriendRequest(){
        $.ajax({
            method: "GET", // type --> method, the HTTP method used for the request.
            url: friend_api_url,  // URL to which the request is sent.
            contentType: 'application/json',  // The MIME type being sent to the server.
            headers:{"X-CSRFToken": csrftoken},  // Key/Value pairs to send along with the request.
            success : function(json) {
                data = json;
                //print(data, "our friend data")
                badge_number.innerHTML = data["size"];
                $("#request-access").hide();
            },  // This function is called if the request is successful. Data is returned from the server.
            error: function (e) {
                console.log("ERROR: ", e);
            }  // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
        });
    }

    function grabUser(){
        $.ajax({
            method: "GET", // type --> method, the HTTP method used for the request.
            url: user_api_url,  // URL to which the request is sent.
            contentType: 'application/json',  // The MIME type being sent to the server.
            headers:{"X-CSRFToken": csrftoken},  // Key/Value pairs to send along with the request.
            success : function(json) {
                user = json;
                $("#request-access").hide();
            },  // This function is called if the request is successful. Data is returned from the server.
            error: function (e) {
                console.log("ERROR: ", e);
            } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
        });
    }
    const badge_number = document.querySelector("#badge_number");
    var csrftoken = getCookie('csrftoken');
    grabUser();
    //grabFriendRequest();
});
