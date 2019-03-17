function getPosts(searchTerm) {
    var promise = fetch('../api/posts');
    promise.then((getJSON) => {
        return getJSON.json();
    })
}

function getAuthors(searchTerm) {
    var promise = fetch('../api.authors');
}