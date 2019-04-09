# NewPee
CMPUT 404 Project, Winter 2019

# Description
NewPee is a new Social Media app, making connecting to your friends more fun and easy! Currently deployed on newpee.herokuapp.com, NewPee allows you to follow your favourite people, make friends, view your friend's social activity, and make your own posts, showing your friends and followers how you are right now. It allows you to connect to new people AND to be even closer to your existing friends. What will you be today with NewPee?

# Using NewPee
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

When a Post is made, a unique ID is made for it, used to access the Post on its unique URL. Each post also has a unique Author, based on whoever created the Post. 

The Author of the Post can set the privacy settings on each post. Those privacy settings are:
* Public: Any NewPee Author can see the Post.
* FOAF: The friends of the Post's Author and the friends of the friends of the Author will be able to see the Post.
* Friends: Only the friends of the Post's Author can see the post.
* Server Friends: Only friends on that server, not on any other server or foreign service connected to NewPee, can see the post.
* Private: Only an Author of the Post Author's choosing can see the post. 
* Server Only: The Post will only appear on the server it was posted on, not all of NewPee.

In addition, a post can be Markdown and/or Unlisted
* Markdown: Allows for the content to be formatted in the Markdown text formatting language.
* Unlisted: Allows for the post to not be displayed on your feed or wall, with other people only being able to see the message if they have the post's URL. 

When the post is clicked on, Authors can add comments to the post, and the post's author can also delete the post. 

There are two other types of Posts: Images and Github posts.

### Images

Images are identical to posts, except for the content, which, instead of being text-based, allows you to attach a picture as the content.

### Github

To make GitHub posts, you have to edit your profile and enter your Github URL. Once you do that, you can make a Github post, which will pull your latest Github activity and turns that into a post. 

* Title: What was done, such as "User Pushed to git-repository".
* Description: Github Activity
* Content: What specifically was done, like "Pushed a commit".

## Feed
Clicking the NewPee logo takes you to your feed, which allows you to see all of the listed posts that have been posted publicly, or by your friends to friends, or by the friends of your friends of FOAF posts, private posts you have been allowed to see, and posts that were posted on the server. This includes image posts and Github posts. This is a good way to see recent posts on Newpee!

## Search
At the top of most pages when you are logged in, there is a header that contains a search bar. Here, you can search for an Author by their username or by part of their username. From there, you can click on their page, follow them, or give a friend request!

## Friend Requests
The icon with two people at the top-right represents the Friend Request page. This is where you can see any friend requests that you have, and either approve or reject them. 

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

