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
            console.log(page_author, "This is the retrieved author.");
            if(page_author.followers.includes(user_id)){
                console.log("Already following");
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
        console.log("This is response", response);
        return response.json();
    })
    .then(function(responseJSON) {
        console.log("This is the JSON: ", responseJSON);
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
        console.log(posts)
    })
}

function subtractUserFriends(){
    data = {};
    data["friends"] = [0];
    console.log(user_author.friends, "Current user friend list")
    //Add all friends back except the current Authors page.
    if(user_author.friends.length != 0){
        for (var authors in user_author.friends){
            if(user_author.friends[authors] != author_uuid && user_author.friends[authors] != 0 && user_author.friends[authors] != user_id){
                console.log(user_author.friends[authors], "pushing ___ user.");
                data["friends"].push(user_author.friends[authors]);
                }
            }
        }
    data["friends"].shift();    // remove the [0]
    console.log(data, "user-subtract");
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
    console.log(data, "author-subtract");
    $.ajax({
        method: "PATCH", // type --> method, the HTTP method used for the request.
        //async: false,
        url: author_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            //console.log(json);
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
            console.log("User friends added")
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
            //console.log(json);
            console.log("Author friends added")
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
    console.log("Remove Friends");
    console.log(user_author.friends, "Current user friend list")
    subtractUserFriends();
    subtractAuthorFriends();
    }
}

grabAuthor();
grabUser();
let posts = getPosts();
// In The future, we should keep these, then every ajax call just updates them depending.
console.log(csrftoken);
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
           console.log(recieving_author);
           // updatefollowersPOST(JSON.stringify(data),enumType); // update the follower list
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
};

function updateNumPostGet(){
    $.ajax({
        method: "GET", // type --> method, the HTTP method used for the request.
        url: author_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        success : function(json) {
            author = json;
            console.log(author);
            author.posts_created += 1;
            var numOfPost = {posts_created : author.posts_created.toString()};
            console.log(JSON.stringify(numOfPost));
            updateNumPostPut(JSON.stringify(numOfPost));
            console.log(author);
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
};

function updateNumPostPut(numOfPost){
    console.log(numOfPost);
    $.ajax({
        method: "PATCH", // type --> method, the HTTP method used for the request.
        //async: false,
        url: author_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: (numOfPost), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            console.log(json);
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
            console.log($(this).attr("id"));
            location.pathname =  $(this).attr("id");
        }
    });
});

function sendFriendRequest(){

    data = {};
    author = {};
    friend = {};
    console.log(sending_author , "send");
    console.log(recieving_author, "rec");
    data["query"] = "friendrequest";
    data["author"] = sending_author;
    data["friend"] = recieving_author;

    $.ajax({
        method: "POST", // type --> method, the HTTP method used for the request.
        //async: false,
        url: "/api/friendrequest", // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
            console.log("requested access complete");
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
    console.log(recieving_author["id"]);
    var split_uuid = recieving_author["id"].split("/")

    url = "/api/author/" +  split_uuid[split_uuid.length-1] + "/decline-friend-request";
    console.log(url, "sending to this url..");

    $.ajax({
        method: "POST", // type --> method, the HTTP method used for the request.
        //async: false,
        url: url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
            console.log("requested access complete");
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
    console.log("This is it: ", page_author.github_url);
    let github_user = page_author.github_url.split('/').pop();
    const response = await fetch('https://api.github.com/users/' + github_user + '/events', {});
    const json = await response.json();
    return json;
}

function makePost(post_title,post_content, post_description, content_type){
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
        content_type : content_type
    };
     //update friends stuff here
    if (radio_value==4){
        data["visible_to"] =  [page_author["id"]];
        data["other_author"] =  other_author_text.innerHTML;        
    }
    if (unlistedBool.checked){
        data["unlisted"] = true;
    }

    data= JSON.stringify(data);
    console.log(data, "OUR DATA FOR POST");

    // Goes to post_created
    // author.view post_created view
    $.ajax({
        method: "POST", // type --> method, the HTTP method used for the request.
        //async: false,
        url: "/api/posts", // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data : data, // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
            updateNumPostGet();
            location.reload();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
}

const elementMakePost = document.querySelector("#post_creation_submit");
elementMakePost.addEventListener('submit', event => {
    event.stopImmediatePropagation();
    event.preventDefault();
  // https://stackoverflow.com/questions/31878960/calling-django-view-from-ajax
    console.log("button clicked");
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



});

//Post picture first, then make post with picture
const elementMakeImagePost = document.querySelector("#btnfileupload");
elementMakeImagePost.addEventListener('submit', event => {
    event.stopImmediatePropagation();
    var post_title = document.querySelector("#image-post-title").value;
    var post_description = document.querySelector("#image-post-comment-description").value;
    var content_type = "image"
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
            post_content =json ;
            makePost(post_title, post_content, post_description, content_type);
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
});

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
            console.log(json);
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
});

const elementUpdateProfile = document.querySelector("#edit_profile_submit");
elementUpdateProfile.addEventListener('submit', event => {
    //event.preventDefault();
    event.stopImmediatePropagation();
    $('#edit_profile_modal').modal('hide');
    var newDisplayName = document.querySelector("#author-display-name").value;
    var newBio = document.querySelector("#author-bio").value;
    var newGitHubURL = document.querySelector("#author-github").value;
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

    console.log(JSON.stringify(data));

    $.ajax({
        method: "PATCH", // type --> method, the HTTP method used for the request.
        url: author_api_url, // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data: JSON.stringify(data), // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            console.log(json);
            $("#request-access").hide();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
});

const elementPullGithub = document.querySelector("#github_api_pull");
elementPullGithub.addEventListener('submit', async event => {
    event.stopImmediatePropagation();
    event.preventDefault();
    var github_data = await github_api();
    console.log("This is the data", github_data);
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

    // console.log(radio_value);
    // if (postType.checked){

    // };

    user_id=  user_id.split("/")[5] ;
    console.log(page_author)
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
        content_type : "text/markdown"
    };

    console.log(user_id);
    if (radio_value==4){
        data["visible_to"] = [user_id];
    }

    // if (postType.checked){
    //     data["content_type"] = postType.value;
    // };
    data= JSON.stringify(data);
    console.log(data, "OUR DATA FOR POST");
    // Goes to post_created
    // author.view post_created view
    $.ajax({
        method: "POST", // type --> method, the HTTP method used for the request.
        //async: false,
        url: "/api/posts", // URL to which the request is sent.
        contentType: 'application/json', // The MIME type being sent to the server.
        headers:{"X-CSRFToken": csrftoken}, // Key/Value pairs to send along with the request.
        data : data, // Data to be sent to the server. Transoformed to query string if not one yet.
        success : function(json) {
            $("#request-access").hide();
            console.log("requested access complete");
            updateNumPostGet();
        }, // This function is called if the request is successful. Data is returned from the server.
        error: function (e) {
            console.log("ERROR: ", e);
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error.
    });
    return false;
});
});