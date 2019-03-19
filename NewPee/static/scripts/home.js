


$(document).ready(function(){

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


function getFileData(myFile){
    var file = myFile.files[0];  
    var filename = file.name;
    console.log(filename);
 }

 var csrftoken = getCookie('csrftoken');



 var author_url = location.pathname;
 var author_uuid = author_url.split("/")[2];
 var author_api_url = "/api" + author_url;
 

 var user_id = document.getElementById("userID").value; // grabbing from hidden value through django context
 var user_api_url = "/api/authors/" + user_id;
 
 console.log(user_api_url)



 function grabAuthor(){


    $.ajax({
        type: "GET",
        async:false,    // wait till we have the author.
        url: author_api_url,
        contentType: 'application/json',
        headers:{"X-CSRFToken": csrftoken},
        success : function(json) {
            page_author = json;
            console.log(page_author, "This is the retrieved author.")
            $("#request-access").hide();
        },
        error: function (e) {      
            console.log("ERROR: ", e);
        }
    });


    }
    

//https://stackoverflow.com/questions/30211605/javascript-html-collection-showing-as-0-length
    
function getPosts() {
    fetch('../api/posts')
    .then(function(response) {
        console.log("This is response", response);
        return response.json();
    })
    .then(function(responseJSON) {
        console.log("This is the JSON: ", responseJSON);
        posts = responseJSON;
    })
    
}

let posts = getPosts();
var page_author;

page_author = grabAuthor();



const follow_submit_form = document.querySelector("#follow_user_submit");
const follow_submit_button = document.querySelector("#follow_user_submit_button");




console.log(csrftoken);


// Update page author profile.
// adding the current logged in user to current authors page followers

function updatefollowersPOST(follower){
    console.log(follower);
    $.ajax({
        type: "PATCH",
        async: false,
        url: author_api_url,
        contentType: 'application/json',
        headers:{"X-CSRFToken": csrftoken},
        data: (follower), 
        success : function(json) {
            console.log(json);
            $("#request-access").hide();
            follow_submit_button.innerHTML = "Unfollow";
        },
        error: function (e) {      
            console.log("ERROR: ", e);
        }
    });
};

// Update your following list
// Patch onto 

function updatefollowingPOST(following){
    console.log(following);
    $.ajax({
        type: "PATCH",
        async: false,
        url: user_api_url,
        contentType: 'application/json',
        headers:{"X-CSRFToken": csrftoken},
        data: (following), 
        success : function(json) {
            console.log(json);
            $("#request-access").hide();
        },
        error: function (e) {      
            console.log("ERROR: ", e);
        }
    });
};


// Get the current followers of the Profile.
// Add 
function updatefollowingGet(){



    $.ajax({
        type: "GET",
        async: false,
        url: user_api_url,
        contentType: 'application/json',
        headers:{"X-CSRFToken": csrftoken},
        success : function(json) {
            author = json;
            //console.log(author);
            var data = {};   
            data["following"] = [author_uuid];
            console.log(author.following, "We are currently following")

            // Only add followers if they have some     
            if(author.following.length != 0){
            
            // go through the page old following
            for (var authors in author.following){
                if(author.following[authors] != author_uuid && author.following[authors] != 0){
                    // push all the old followers onto the patch.
                    data["following"].push(author.following[authors]);

                    }  
                }
            }


            updatefollowingPOST(JSON.stringify(data)); // update the follower list


            $("#request-access").hide();
        },
        error: function (e) {      
            console.log("ERROR: ", e);
        }
    });
};





// Get the current followers of the Profile.
// Add 
function updatefollowersGet(){
    $.ajax({
        type: "GET",
        async: false,
        url: author_api_url,
        contentType: 'application/json',
        headers:{"X-CSRFToken": csrftoken},
        success : function(json) {
            author = json;
            //console.log(author);
            var data = {};

            var user_id = document.getElementById("userID").value; // grabbing from hidden value through django context

            console.log(user_id, "Logged in user id.")

            
            
            data["followers"] = [user_id];

            console.log(data, "Data Beforehand.")
            //console.log(author.followers, "Current followers")

            // Only add followers if they have some     
            if(author.followers.length != 0){
            
            // go through the page old followers
            for (var authors in author.followers){

                //console.log(author.followers[authors], "adding author..");

                if(author.followers[authors] != user_id && author.followers[authors] != 0){
                    // push all the old followers onto the patch.

                    //console.log(author.followers[authors], "pushing onto stack.")
                    data["followers"].push(author.followers[authors]);

                    }  
                }
            }

            console.log(data, "Data afterwards.")


            updatefollowersPOST(JSON.stringify(data)); // update the follower list
            //console.log(author);      


            $("#request-access").hide();
        },
        error: function (e) {      
            console.log("ERROR: ", e);
        }
    });
};





function updateNumPostGet(){
    $.ajax({
        type: "GET",
        url: author_api_url,
        contentType: 'application/json',
        headers:{"X-CSRFToken": csrftoken},
        success : function(json) {
            author = json;
            console.log(author);
            author.posts_created += 1;
            var numOfPost = {posts_created : author.posts_created.toString()};
            console.log(JSON.stringify(numOfPost));
            updateNumPostPut(JSON.stringify(numOfPost));
            console.log(author);      
            $("#request-access").hide();
        },
        error: function (e) {      
            console.log("ERROR: ", e);
        }
    });
};

function updateNumPostPut(numOfPost){
    console.log(numOfPost);
    $.ajax({
        type: "PATCH",
        async: false,
        url: author_api_url,
        contentType: 'application/json',
        headers:{"X-CSRFToken": csrftoken},
        data: (numOfPost), 
        success : function(json) {
            console.log(json);
            $("#request-access").hide();
        },
        error: function (e) {      
            console.log("ERROR: ", e);
        }
    });
};
    



// https://blog.teamtreehouse.com/creating-autocomplete-dropdowns-datalist-element

// Get the <datalist> and <input> elements.
var dataList = document.getElementById('ajax_authors');
var input = document.getElementById('ajax');


var delay = (function(){
    var timer = 0;
    return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
   };
})();

$(input).keyup(function() {
    delay(function(){
        fetch('../api/authors').then(function(response) {
            return response.json();
        }).then(function (JSONresponse) {
            JSONresponse.forEach(function(item) {
                    // Create a new <option> element.
                    let option = document.createElement('option');
                    link = document.createAttribute("value");
                    link.value = "authors/"+String(item.id);
                    option.setAttributeNode(link);
                    // Set the value using the item in the JSON array.
                    option.value = JSONresponse.user;
                    // Add the <option> element to the <datalist>.
                    dataList.appendChild(option);
            })
        })
    }, 1000);
});

$('a[data-toggle="modal"]').click(function(){
    window.location.hash ="khkhajge";
});

function revertToOriginalURL() {
    var original = window.location.href.substr(0, window.location.href.indexOf('#'))
    history.replaceState({}, document.title, original);
}

$('.modal').on('hidden.bs.modal', function () {
    revertToOriginalURL();
});


function callFollowers(){
    updatefollowingGet();
}

function callFollowing(callback){

    updatefollowersGet();
    callback();
}




follow_submit_form.addEventListener('submit', event =>{

    event.preventDefault();

    //updatefollowersGet();
    //updatefollowingGet();


    callFollowing(callFollowers);





    //alert("button clicked");

});




const elementMakePost = document.querySelector("#post_creation_submit");

elementMakePost.addEventListener('submit', event => {
  event.preventDefault();
  // https://stackoverflow.com/questions/31878960/calling-django-view-from-ajax
    console.log("button clicked");
    var request_data = "Data"; // TODO: include all post data

    var post_title = document.querySelector("#post-title").value;
    var post_content = document.querySelector("#post-comment-content").value;
    var post_description = document.querySelector("#post-comment-description").value;
    var radioButtons = document.getElementsByName("friends-radio-option");
    console.log(radio_value);


    var radio_value;

    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked){
            radio_value = radioButtons[i].value;
        }
    }

    var data = JSON.stringify({ 
        title : post_title,
        author : author_uuid,
        content : post_content,
        description : post_description,
        csrfmidddlewaretoken: csrftoken,
        privacy : radio_value,

    });

    console.log(data, "OUR DATA FOR POST");

    // Goes to post_created
    // author.view post_created view

    $.ajax({
        type: "POST",
        async: false,
        url: "/api/posts/",
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

const elementUpdateProfile = document.querySelector("#edit_profile_submit");
elementUpdateProfile.addEventListener('submit', event => {
    event.preventDefault();
    $('#edit_profile_modal').modal('hide');
    var newDisplayName = document.querySelector("#author-display-name").value;
    var newBio = document.querySelector("#author-bio").value;
    var newGitHubURL = document.querySelector("#author-github").value;
    
    var data = {}
    if (newDisplayName){
        data["displayName"] = newDisplayName;
    }
    if (newBio){
        data["bio"] = newBio;
    }
    if (newGitHubURL){
        data["github_url"] = newGitHubURL;
    }

    

    console.log(JSON.stringify(data));


    $.ajax({
        type: "PATCH",
        url: author_api_url,
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

});  
});  
