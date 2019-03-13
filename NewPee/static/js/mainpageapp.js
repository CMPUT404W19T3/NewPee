
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

const element = document.querySelector("#post_creation_submit")


https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
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





element.addEventListener('submit', event => {
  event.preventDefault();
  // actual logic, e.g. validate the form
  alert('Form submission cancelled.');

  var csrftoken = getCookie('csrftoken');
  console.log(csrftoken);

  // https://stackoverflow.com/questions/31878960/calling-django-view-from-ajax
    console.log("button clicked");
    var request_data = "Data"; // TODO: include all post data


    var post_title = document.querySelector("#post-title").value;
    var post_content = document.querySelector("#post-comment-content").value;
    var post_description = document.querySelector("#post-comment-description").value;
    var radioButtons = document.getElementsByName("friends-radio-option");


    var radio_value;

    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked){
            radio_value = radioButtons[i].value;
        }
    }


    console.log(radio_value);





    // Goes to post_created
    // author.view post_created view

    $.ajax({
        type: "POST",
        url: "/api/posts/",
        data : { 
            title : post_title,
            author : 'hello',
            content : post_content,
            description : post_description,
            csrfmidddlewaretoken: csrftoken,
            privacy : radio_value,

        },



        success : function(json) {
            $("#request-access").hide();
            console.log("requested access complete");

        }
    })
});


});



