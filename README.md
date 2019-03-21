# NewPee
CMPUT 404 Project, Winter 2019

# Web Service API
When starting NewPee for the first time on a browser, you are taken to the login page (/login). Here, you can log on to NewPee, or sign up if you don't have an account. 

The signup link takes you the signup page (/signup). Entering in your first and last name, username, and password, so long as the username's not in current use, will create your account.

## Profile
Once logged in or signed up, you are taken to your unique Authors page (/authors/{author_id}). Eah NewPee user is an Author, and this is your profile page. Here, you can perform a variety of actions.

* Edit your profile, including changing your display name, adding or changing your Bio, and adding or changing your GitHub URL. 
* See how many posts you have, how many people are following you and who they are, and how many people you follow and who they are. 
* View and change your profile picture. 
* View Posts that you made.
* Make Posts.

## Posts
Posts are the main form of content on NewPee. Each Post can have:
* a title (max length = 30 characters)
* a description (max length = 150 characters)
* content (text-based)
* an image

When a Post is made, a unique ID is made for it, used to access the Post on its unique URL. Each post also has a unique Author, based on whoever created the Post. 

The Author of the Post can set the privacy settings on each post. Those privacy settings are:
* Public: Any NewPee Author can see the Post.
* FOAF: The friends of the Post's Author and the friends of the friends of the Author will be able to see the Post.
* Friends: Only the friends of the Post's Author can see the post.
* Private: Only the Author of the Post can see the Post.
* Server Only: The Post will only appear on the server it was posted on, not all of NewPee.

On these Posts, other Authors (as well as the Post's original Author) can add Comments to the bottom of the post.

## Search
At the top of most pages when you are logged in, there is a header that contains a search bar. When you search a term, it searches for:

* Posts, looking for the term in the title, description, content, or the author.
* Author, looking for the term in the username, first or last name, or display name.

Searching for Posts and Authors is a good way to find a Post that you want to comment on, or an Author that you want to follow or request to be friends with.

# References
* [Seperating models out](https://stackoverflow.com/questions/5534206/how-do-i-separate-my-models-out-in-django)
* [Adjusting __init__.py](https://stackoverflow.com/questions/13718656/can-i-divide-the-models-in-different-files-in-django)
* [Using UUID](https://stackoverflow.com/questions/32528224/how-to-use-uuid-in-django)
* [Relationships in Django](https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.ManyToManyField)
* [Extending User Model](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
)
* [Customizing User Model](https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)
* [Adding icons](https://fontawesome.com/start)
* [Adding search box in the header](http://code-chunk.com/chunks/5746559c9acf7/simple-html-css-search-box)

