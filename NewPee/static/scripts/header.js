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



var user_id = document.getElementById("userID").value; // grabbing from hidden value through django context
var user_api_url = "/api/authors/" + user_id;


function grabUser(){

    $.ajax({
        type: "GET",
        url: user_api_url,
        contentType: 'application/json',
        headers:{"X-CSRFToken": csrftoken},
        success : function(json) {
            user = json;
            console.log(user);
            var notifications = 0;
            for (var authors in user.followers){
                if( !user.friends.includes( user.followers[authors])){
                        notifications++;
                    }
                }
            badge_number.innerHTML = notifications;
            $("#request-access").hide();
        },
        error: function (e) {      
            console.log("ERROR: ", e);
        }
    });
}

var author_url = location.pathname;
const badge_number = document.querySelector("#badge_number");
var csrftoken = getCookie('csrftoken');

grabUser();

});  

