
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
console.log(author_url);
var author_api_url = "/api" + author_url;
console.log(author_api_url);
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
            var numOfPost = "{'posts_created' :'" + author.posts_created.toString() + "'}";
            console.log(JSON.stringify(numOfPost));
            updateNumPostPut(numOfPost);
            console.log(author);
            $("#request-access").hide();
        },
        error: function (e) {      
            console.log("ERROR: ", e);
        }
    });
};

function updateNumPostPut(numOfPost){
    $.ajax({
        type: "PATCH",
        url: author_api_url,
        headers:{"X-CSRFToken": csrftoken},
        data: (JSON.stringify(numOfPost)), 
        success : function(json) {
            console.log(json);
            $("#request-access").hide();
        },
        error: function (e) {      
            console.log("ERROR: ", e);
        }
    });
};
    



const element = document.querySelector("#post_creation_submit")


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

element.addEventListener('submit', event => {
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
        author : 'hello',
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


});



