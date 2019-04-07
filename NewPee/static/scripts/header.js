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
var user_id = document.getElementById("userIDSpan");
var user_id = document.getElementById("userID").value; // grabbing from hidden value through django context
var user_id_spliced = user_id.split("/");
console.log(user_id);
var user_api_url = "/api/authors/" + user_id_spliced[user_id_spliced.length-1];
var friend_api_url =   "/api/author/"+ user_id_spliced[user_id_spliced.length-1] +  "/friendrequest"
console.log(friend_api_url);
console.log(user_api_url);

function grabFriendRequest(){
    $.ajax({
        type: "GET",
        url: friend_api_url,
        contentType: 'application/json',
        headers:{"X-CSRFToken": csrftoken},
        success : function(json) {
            data = json;
            //print(data, "our friend data")         
            badge_number.innerHTML = data["size"];
            $("#request-access").hide();
        },
        error: function (e) {
            console.log("ERROR: ", e);
        }
    });
}

function grabUser(){
    $.ajax({
        type: "GET",
        url: user_api_url,
        contentType: 'application/json',
        headers:{"X-CSRFToken": csrftoken},
        success : function(json) {
            user = json;
            console.log(user);
            $("#request-access").hide();
        },
        error: function (e) {
            console.log("ERROR: ", e);
        }
    });
}
const badge_number = document.querySelector("#badge_number");
var csrftoken = getCookie('csrftoken');
grabUser();
//grabFriendRequest();



});
