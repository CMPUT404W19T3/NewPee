

from Authors.models import Author
from django.contrib.auth.models import User
from Posts.models import Post, Comment



class GeneralBuilding:


    def create_author(self, username="temp_user", displayName = "temp_name", email="temp@gmail.com", password="TestPass1"):


        user = User.objects.create(username=username, email=email, password=password)
        user.save()
        author = Author.objects.create(user=user, displayName=displayName)

        return author



    def create_authors(usernames):

        for username in usernames:
            email= username + '@gmail.com'
            displayName =  username
            GeneralBuilding.create_author(username=username, email= email, displayName = displayName)


    def create_post(self, title, author):

        post = Post.objects.create(title=title, author=author, content="body")
        post.save()

        return post



Factory = GeneralBuilding()

