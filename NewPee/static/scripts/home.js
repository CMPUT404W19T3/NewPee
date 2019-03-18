
function getFileData(myFile){
    var file = myFile.files[0];  
    var filename = file.name;
    console.log(filename);
 }

//https://stackoverflow.com/questions/30211605/javascript-html-collection-showing-as-0-length
$(document).ready(function(){
    
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

var author_url = location.pathname;
var author_uuid = author_url.split("/")[2];
var author_api_url = "/api" + author_url;

var csrftoken = getCookie('csrftoken');
console.log(csrftoken);




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

    console.log(data);

    // Goes to post_created
    // author.view post_created view

    $.ajax({
        type: "POST",
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
