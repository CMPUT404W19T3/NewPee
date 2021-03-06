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

var author_url = location.pathname;
var author_uuid = author_url.split("/")[2];
var author_api_url = "/api" + author_url;
var FriendsEnum = Object.freeze({"Add":1, "Subtract":2, });
const follow_submit_form = document.querySelector("#follow_user_submit");
const follow_submit_button = document.querySelector("#follow_user_submit_button");
var sending_author;
var recieving_author;
var page_author;
var user_author;

var csrftoken = getCookie('csrftoken');
var author_url = location.pathname;
var author_uuid = author_url.split("/")[2];
var author_api_url = "/api" + author_url;
var user_id = document.getElementById("userID").value; // grabbing from hidden value through django context
user_id = author_url.split("/");
user_id = user_id[user_id.length-1];
var user_id = document.getElementById("userIDSpan");
var user_id = document.getElementById("userID").value; // grabbing from hidden value through django context
var user_api_url = user_id;

function grabUser(){
    $.ajax({
        method: "GET", // type --> method, the HTTP method used for the request.
        url: author_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        success : function(json) {
          stripped_user_id=  json["id"].split("/")[5] ;
            user_author = json;
            user_author["id"] = stripped_user_id;
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
}
 function grabAuthor(){
    $.ajax({
        method: "GET", // type --> method, the HTTP method used for the request.
        //async:false,    // wait till we have the author.
        url: author_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        success : function(json) {
            page_author = json;
            stripped_user_id=  json["id"].split("/")[5] ;
            page_author["id"] = stripped_user_id;
            if(page_author.followers.includes(user_id)){
                follow_submit_button.innerHTML = "Unfollow";
            }
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
    }

//https://stackoverflow.com/questions/30211605/javascript-html-collection-showing-as-0-length
function getPosts() {
    fetch('../api/posts')
    .then(function(response) {
        return response.json();
    })
    .then(function(responseJSON) {
        posts = responseJSON;
        temp_posts = posts;
        for (var post in posts){
            if (posts[post].visibility === "FRIENDS") {
                if (!page_author.friends.includes(user_author.id))
                delete temp_posts[post];
                var postID = "posts/" + temp_posts[post].id;
                document.getElementById(postID).style.visibility="hidden";
                html_post.style.visibility = "hidden";
                continue;
            }
            if (posts[post].visibility === "PRIVATE"){
                if(posts[post].visible_to != user_author.id && page_author.id != user_author.id){
                    //delete temp_posts[post];
                    var postID = "posts/" + posts[post].id;
                    document.getElementById(postID).style.visibility="hidden";
                    continue;
                }
            }
        }
        posts= temp_posts;
    })
}

function subtractUserFriends(){
    data = {};
    data["friends"] = [0];
    //Add all friends back except the current Authors page.
    if(user_author.friends.length != 0){
        for (var authors in user_author.friends){
            if(user_author.friends[authors] != author_uuid && user_author.friends[authors] != 0 && user_author.friends[authors] != user_id){
                data["friends"].push(user_author.friends[authors]);
                }
            }
        }
    data["friends"].shift();    // remove the [0]
    $.ajax({
        method: "PATCH", // type --> method, the HTTP method used for the request.
        //async: false,
        url: user_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
}

function subtractAuthorFriends(){
    data ={};
    data["friends"] = [0];
    if(page_author.friends.length != 0){
        for (var authors in page_author.friends){
            if(page_author.friends[authors] != user_id && page_author.friends[authors] != 0 && user_author.friends[authors] != author_uuid){
                data["friends"].push(page_author.friends[authors]);
                }
            }
        }
    data["friends"].shift();    // remove the [0]
    $.ajax({
        method: "PATCH", // type --> method, the HTTP method used for the request.
        //async: false,
        url: author_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
}

function addUserFriends(){
    data = {};
    data["friends"] = [author_uuid];
    if(user_author.friends.length != 0){
        for (var authors in user_author.friends){
            if(user_author.friends[authors] != author_uuid && user_author.friends[authors] != 0){
                data["friends"].push(user_author.friends[authors]);
                }
            }
        }
    $.ajax({
        method: "PATCH", // type --> method, the HTTP method used for the request.
        //async: false,
        url: user_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
}

function addAuthorFriends(){
    data ={};
    data["friends"] = [user_id];
    if(page_author.friends.length != 0){
        for (var authors in page_author.friends){
            if(page_author.friends[authors] != user_id && page_author.friends[authors] != 0){
                data["friends"].push(page_author.friends[authors]);
                }
            }
        }
    $.ajax({
        method: "PATCH", // type --> method, the HTTP method used for the request.
        //async: false,
        url: author_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
}

function updateFriends(enumType) {
    if (enumType===FriendsEnum.Add){
    addUserFriends();
    addAuthorFriends();
    }
    if (enumType===FriendsEnum.Subtract){
        subtractUserFriends();
        subtractAuthorFriends();
    }
}

grabAuthor();
grabUser();
//let posts = getPosts();
// In The future, we should keep these, then every ajax call just updates them depending.
// Get the current followers of the Profile.
// Add the clicked author to your following list.


function getSenderAuthorData(enumType){
    $.ajax({
        method: "GET", // type --> method, the HTTP method used for the request.
        async: false, // Synchronous request.
        url: user_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        success : function(json) {
           sending_author = json;
            //updatefollowingPOST(JSON.stringify(data),enumType); // update the follower list
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
};

// Get the current followers of the Profile.
// Add
function getrecivingAuthorData(enumType){
    $.ajax({
        method: "GET", // type --> method, the HTTP method used for the request.
        async: false, // Synchronous request.
        url: author_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        success : function(json) {
           recieving_author = json;
           // updatefollowersPOST(JSON.stringify(data),enumType); // update the follower list
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
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

$(document).ready(function(){
    $(".card").click(function(evt){
        if ($(this).attr("id")){
            location.pathname =  $(this).attr("id");
        }
    });
});





















function sendFriendRequest(){

    data = {};
    author = {};
    friend = {};

    console.log(sending_author, "sending");
    console.log(recieving_author, "recieving");

    data["query"] = "friendrequest";
    data["author"] = sending_author;
    data["friend"] = recieving_author;
    data["type"] = "local_add";

    console.log(JSON.stringify(data));


    $.ajax({
        method: "POST", // type --> method, the HTTP method used for the request.
        //async: false,
        url: "/api/friendrequest", // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {

            console.log("Friend request sent");

            $("#request-access").hide();
            $("#follow_user_submit_button").html("Unfollow");
            const followers_stat = document.querySelector("#follower_stat");
            $("#follower_stat").html(Number(followers_stat.innerHTML) + 1) ;
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
}

function sendUnfollowRequest(){

    data = {};
    data["query"] = "unfollow";
    data["author"] = sending_author;
    data["friend"] = recieving_author;
    var split_uuid = recieving_author["id"].split("/")
    url = "/api/author/" +  split_uuid[split_uuid.length-1] + "/decline-friend-request";

    $.ajax({
        method: "POST", // type --> method, the HTTP method used for the request.
        //async: false,
        url: url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
            const followers_stat = document.querySelector("#follower_stat");
            $("#follower_stat").html(Number(followers_stat.innerHTML) -1 ) ;
            $("#follow_user_submit_button").html("Follow");
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
}

// Functions for adding
function callRecievingData(){
    getrecivingAuthorData(FriendsEnum.Add);
}

function callSenderData(callback){
    getSenderAuthorData(FriendsEnum.Add);    // Call second, friends piggybacks off Followers
    callback();
}

try {
follow_submit_form.addEventListener('submit', event =>{
    event.preventDefault();
    event.stopImmediatePropagation();
    var follow_unfollow_text = follow_submit_button.textContent || follow_submit_button.innerText;
    callSenderData(callRecievingData);
    if(follow_unfollow_text === "Follow"){
        sendFriendRequest();
    }
    else{
        sendUnfollowRequest();
    }
});
}
catch{
}

// Determine which data we would like to display.
async function github_api() {
    grabAuthor();
        // const response = await fetch('some-url', {});
        // const json = await response.json();
        // return json.first_name.concat(' ').concat(json.last_name);
    let github_user = page_author.github_url.split('/').pop();
    const response = await fetch('https://api.github.com/users/' + github_user + '/events', {});
    const json = await response.json();
    return json;
}

async function makePost(post_title,post_content, post_description, contentType){
    var radio_value;
    var radioButtons = document.getElementsByName("friends-radio-option");
    var unlistedBool = document.getElementById("unlisted");
    var VisiblityEnum = Object.freeze({1:"PUBLIC", 2:"FOAF", 3:"FRIENDS", 4:"PRIVATE", 5:"SERVERONLY", 6:"SERVERFRIENDS"})
    var visible_to;
    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked){
            radio_value = radioButtons[i].value;
        }
    }
    var data = {
        title : post_title,
        author : page_author["id"],
        content : post_content,
        description : post_description,
        csrfmidddlewaretoken: csrftoken,
        visibility : VisiblityEnum[radio_value],
        visible_to : visible_to,
        contentType : contentType
    };
     //update friends stuff here
    if (radio_value==4){
        data["visible_to"] =  [page_author["id"]];
        if (other_author_text){
            data["visible_to"].push(other_author_text.innerHTML);
        } 
    }

    console.log(data["visible_to"]);
    if (unlistedBool.checked){
        data["unlisted"] = true;
    }

    data= JSON.stringify(data);

    // Goes to post_created
    // author.view post_created view
    await $.ajax({
        method: "POST", // type --> method, the HTTP method used for the request.
        //async: false,
        url: "/api/posts", // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data : data, // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
            //location.reload();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
}

try {
    const elementMakePost = document.querySelector("#post-btn");


    elementMakePost.addEventListener('click', event => {
    event.stopImmediatePropagation();
    event.preventDefault();
  // https://stackoverflow.com/questions/31878960/calling-django-view-from-ajax
    var post_title = document.querySelector("#post-title").value;
    var post_content = document.querySelector("#post-comment-content").value;
    var post_description = document.querySelector("#post-comment-description").value;
    var postType = document.getElementById("markdown");
    var post_type
    if (postType.checked){
        post_type = postType.value;
    }else{
        post_type = "text/plain";
    };

    makePost(post_title,post_content, post_description, post_type);

    var radioButtons = document.getElementsByName("friends-radio-option");
    radioButtons[0].checked = true;

    document.getElementById("post-title").value = "";
    document.getElementById("post-comment-description").value = "";
    document.getElementById("post-comment-content").value = "";
})
} catch (error) {
    console.log("on another users profile.");
};


try {
    const elementMakeImagePost = document.querySelector("#btnfileupload");
    elementMakeImagePost.addEventListener('submit', async event => {
    event.preventDefault();
    event.stopImmediatePropagation();
    var post_title = document.querySelector("#image-post-title").value;
    var post_description = document.querySelector("#image-post-comment-description").value;
    var contentType = "image"
    var form = document.getElementById('imageupload');
    var formData = new FormData(form);
    $.ajax({
        url : "/api/image/", // URL to which the request is sent.
        method: "POST", // type --> method, the HTTP method used for the request.
        data : formData, // Data to be sent to the server. Transoformed to query string if not one yet.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        processData: false, // For non-processed data, like a DOMDocument or something which is not a string (i.e. image).
        contentType: false, // The MIME type being sent to the server.
        success : function(json) {
            post_content = json ;
            makePost(post_title, post_content, post_description, contentType);
            //location.reload()
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
    });
} catch (error) {
    console.log("on another users profile.");
}





//Post picture first, then make post with picture

// const elementUpdateProfilePic = document.querySelector("#button");
// elementUpdateProfilePic.addEventListener('click', uploadImage);
// function uploadImage() {
//     $('#select-profile-pic').trigger('click');
// }


const private_author_share = document.querySelector("#PrivatePrivacy");
const private_author_text = document.querySelector("#private-author");


$('input[type="radio"]').click(function(){
    var demovalue = $(this).val();

    if (demovalue == 4){
        private_author_text.hidden = false;
    }
    else{
        private_author_text.hidden = true;
        other_author_text.hidden = true;
        other_author_start_text.hidden = true;
    }
});


const other_author_text = document.getElementById("other_author");
const other_author_start_text = document.getElementById("other_author_start_text");

other_author_start_text
function tog(v){return v?'addClass':'removeClass';}
$(document).on('input', '.clearable', function(){
    $(this)[tog(this.value)]('x');
}).on('mousemove', '.x', function( e ){
    $(this)[tog(this.offsetWidth-18 < e.clientX-this.getBoundingClientRect().left)]('onX');
}).on('touchstart click', '.onX', function( ev ){
    ev.preventDefault();
    other_author_text.innerHTML = this.value;
    other_author_text.hidden = false;
    other_author_start_text.hidden = false;

    $(this).removeClass('x onX').val('').change();
});



const elementUpdateProfilePic = document.getElementById("change_profile_pic_submit");
elementUpdateProfilePic.addEventListener('submit', event => {
    event.preventDefault()
    event.stopImmediatePropagation();
    $('#change_profile_pic_modal').modal('hide');

    var newProfilePic = document.getElementById("select-profile-pic").value;

    var data = {
        "image": newProfilePic
    }
    $.ajax({
        method: "PUT", // type --> method, the HTTP method used for the request.
        url: author_api_url, // URL to which the request is sent.
        contentType: "application/json", // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: data, // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
            location.reload();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
});

const elementUpdateProfile = document.querySelector("#edit_profile_submit");
elementUpdateProfile.addEventListener('submit', event => {
    event.preventDefault();
    event.stopImmediatePropagation();
    $('#edit_profile_modal').modal('hide');
    var newDisplayName = document.querySelector("#edit-author-display-name").value;
    var newBio = document.querySelector("#edit-author-bio").value;
    var newGitHubURL = document.querySelector("#edit-author-github").value;
    //var newProfilePic = document.querySelector("#author-profile-pic").value;

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

    $.ajax({
        method: "PATCH", // type --> method, the HTTP method used for the request.
        url: author_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        cache: false,
        success : function(json) {
            $("#request-access").hide();
            location.reload();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
});

try {
    const elementPullGithub = document.querySelector("#github_api_pull");
    elementPullGithub.addEventListener('submit', async event => {
    event.stopImmediatePropagation();
    event.preventDefault();
    var github_data = await github_api();

    if (github_data.message === "Not Found"){
        alert("Github URL is invalid.");
        return;
    }

    // https://stackoverflow.com/questions/31878960/calling-django-view-from-ajax
    var post_title;
    var post_content = '<ul>';
    if (github_data[0].type === "PushEvent") {
        post_title = github_data[0].actor.display_login + " Pushed to " + github_data[0].repo.name;
        for (let index of github_data[0].payload.commits) {
            post_content += '<li>' + index.message + '</li>';
        }
    }
    if (github_data[0].type === "DeleteEvent") {
        post_title = github_data[0].actor.display_login + " Deleted " + github_data[0].repo.name;

        for (let index of github_data[0].payload.commits) {
            post_content += '<li>' + index.message + '</li>';
        }
    }
    if (github_data[0].type === "IssuesEvent") {
        post_title = github_data[0].actor.display_login + " Issue Activity " + github_data[0].repo.name;
        post_content += '<li>' + "Issue Activity" + '</li>';
    }
    post_content += '</ul>'

    var post_description = "Github Activity";
    var github_id = github_data[0].id;
    var radioButtons = document.getElementsByName("friends-radio-option");
    var radio_value;

    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked){
            radio_value = radioButtons[i].value;
        }
    }


    user_id=  user_id.split("/")[5] ;
    var VisiblityEnum = Object.freeze({1:"PUBLIC", 2:"FOAF", 3:"FRIENDS", 4:"PRIVATE", 5:"SERVERONLY"})
    var visible_to;

    var data = {
        title : post_title,
        author : page_author["id"],
        content : post_content,
        description : post_description,
        github_id : github_id,
        csrfmidddlewaretoken: csrftoken,
        visibility : VisiblityEnum[radio_value],
        visible_to : visible_to,
        contentType : "text/markdown"
    };

    if (radio_value==4){
        data["visible_to"] = [user_id];
    }


    data= JSON.stringify(data);
    // Goes to post_created
    // author.view post_created view
    await $.ajax({
        method: "POST", // type --> method, the HTTP method used for the request.
        //async: false,
        url: "/api/posts", // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data : data, // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
            location.reload();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
    return false;
});
} catch (error) {
    console.log("github hidden on others profile");
}

});
