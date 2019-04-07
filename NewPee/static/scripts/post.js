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
    const editPostButton = document.querySelector("#edit_Post_Button");
    var author;






    editPostButton.addEventListener('click', event =>{

    });



    deletePostButton.addEventListener('click', event =>{
        //event.preventDefault();
        console.log(userUUID);
        console.log(userID);
        console.log("DELETING");


        $.ajax({
            type: "GET",
            url: userID,
            contentType: 'application/json',
            headers:{"X-CSRFToken": csrftoken},
            success : function(json) {
                author = json;
                console.log(author.posts_created);
                var data = {};
                data["posts_created"] = author.posts_created - 1;
                console.log(JSON.stringify(data));

                $.ajax({
                    type: "PATCH",
                    url: userID,
                    contentType: 'application/json',
                    headers:{"X-CSRFToken": csrftoken},
                    data: JSON.stringify(data),
                    success : function(json) {
                        console.log(json);
                        $("#request-access").hide();
                    },
                    error: function (e) {
                        console.log("ERROR: ", e);
                    }
                });
                $("#request-access").hide();
            },
            error: function (e) {
                console.log("ERROR: ", e);
            }
        });


        $.ajax({
            type: "DElETE",
            async: false,
            url: "/api/posts/"+post_uuid,
            contentType: 'application/json',
            headers:{"X-CSRFToken": csrftoken},
            success : function(json) {
                $("#request-access").hide();
                console.log("requested access complete");
            },
            error: function (e) {
                console.log("ERROR: ", e);
            }
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
            type: "POST",
            async: false,
            url: "/api/comments",
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
