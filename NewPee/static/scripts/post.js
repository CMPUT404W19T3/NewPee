//https:docs.djangoproject.com/en/dev/ref/csrf/#ajax
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
    
    const elementMakeComment = document.getElementById("comment_creation_submit");
    const authorUUID = document.getElementById("userID").value;

    elementMakeComment.addEventListener('submit', event => {
        
        event.preventDefault();
        // https://stackoverflow.com/questions/31878960/calling-django-view-from-ajax
        
        var postID = location.pathname.split("/")[2];

        var comment = document.querySelector("#comment").value;
        var data = JSON.stringify({
            parent: postID,
            author : authorUUID,
            content: comment,
            csrfmidddlewaretoken: csrftoken,
        });

        console.log(data);
            
        // Goes to post_created
        // author.view post_created view
            
        $.ajax({
            type: "POST",
            async: false,
            url: "/api/comments/",
            contentType: 'application/json',
            headers:{"X-CSRFToken": csrftoken},
            data : data,
            success : function(json) {
                $("#request-access").hide();
                console.log("requested access complete");
            },
            error: function (e) {       
                console.log("ERROR: ", e);
            }
        });
    });


});