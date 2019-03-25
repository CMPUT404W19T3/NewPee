import { getCookie } from 'cookie'; 

var csrftoken = getCookie('csrftoken');

var post_url = location.pathname;
var post_uuid = post_url.split("/")[2];

console.log(post_uuid)


$(document).ready(function(){
    
    const elementMakeComment = document.getElementById("comment_creation_submit");
    const authorUUID = document.getElementById("userID").value;

    const deletePostButton = document.querySelector("#remove_post_submit");

    deletePostButton.addEventListener('submit', event =>{

        console.log("DELETING");
     
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


    });


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