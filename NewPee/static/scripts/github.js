const elementPullGithub = document.querySelector("#github_api_pull");
elementPullGithub.addEventListener('submit', event => {
    event.stopImmediatePropagation();
    //event.preventDefault();
    var github_data = github_api();
    console.log(github_data);
    // https://stackoverflow.com/questions/31878960/calling-django-view-from-ajax
    var post_title = github_data[0].actor.display_login + github_data[0].type;
    var post_content = github_data[0].repo.name;
    var post_description = github_data[0].repo.name;
    var github_id = github_data[0].id;
    var radioButtons = document.getElementsByName("friends-radio-option");

    var radio_value;

    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked){
            radio_value = radioButtons[i].value;
        }
    }

    console.log(radio_value);
    if (postType.checked){
    };
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
        content_type : "text/plain"
    };

    console.log(user_id);

    if (radio_value==4){
        data["visible_to"] = [user_id];
    }

    if (postType.checked){
        data["content_type"] = postType.value;
    };

    data= JSON.stringify(data);
    console.log(data, "OUR DATA FOR POST");

    // Goes to post_created
    // author.view post_created view
    $.ajax({
        method: "POST", // type --> method, the HTTP method used for the request.
        url: "/api/posts/", // URL to which the request is sent.
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
        } // This function is called if the request fails. Data is returned from the server. Returns a dscription of the error
    });
    return false;
});