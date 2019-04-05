from django.db import models
from django_q.tasks import async_task, result

import Authors.models #import Author, ForeignAuthor
import Posts.models #import Post, ForeignPost
import requests
import uuid

class Server(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1000, null=False, blank=False)
    host = models.URLField(max_length=1000, unique=True)
    author_endpoint = models.URLField(max_length=1000, unique=True)
    posts_endpoint = models.URLField(max_length=1000, unique=True)
    friend_endpoint = models.URLField(max_length=1000, unique=True, default="api/friends")
    username = models.CharField(max_length=140, null=False, blank=False, default="testuser")
    password = models.CharField(max_length=140, null=False, blank=False, default="test_pass")
    isActive = models.BooleanField(default=True)

    def getUsername(self):

        return self.username

    def getPassword(self):

        return self.password

    def isServerActive(self):

        return self.isActive

    def createAuthors(self,data):

        for authors in task.result['authors']:

            author_uuid = authors["id"]
            firstname = authors["firstname"]
            lastname = authors["lastname"]
            email= authors["email"]

            if ( Author.objects.filter(id=author_uuid)):

                pass

    def retrieveAuthors(self):

        URL = self.posts_endpoint
        location = self.name

        PARAMS = {
            'username': self.username,
            'password': self.password
        }

        print(self.username, self.password, URL)

        session = requests.Session()
        session.auth = (self.username, self.password)
        r = session.get(url= URL)
        data = r.json()

        print(data, "our data retrieved")

        foreign_post = (data["posts"])

        for post in foreign_post:

            foreign_author = post["author"]
            foreign_author_uuid = foreign_author["id"].split("/")[-1]

            # only pavlov server works right now.

            if(foreign_author["id"].split("/")[2] != "social.hydrated.app"):

                continue

            try:

                Author.objects.get(id = foreign_author_uuid)
                
            except Author.DoesNotExist:

                request2 = session.get(url = foreign_author["id"],)

                print(foreign_author["id"])
                data2 = request2.json()
                print(data2)

                try:

                    print("sideways", data2["id"].split("/")[-1])

                    new_id = (data2["id"].split("/")[-1])
                    Author.objects.get(id = (data2["id"].split("/")[-1]))

                except Author.DoesNotExist:

                    id = data2["id"].split("/")[-1]
                    host = data2["host"]
                    url = data2["url"]
                    displayName = data2["displayName"]
                    friends = data2["friends"]

                    #print(id,host,url,displayName,friends)

                    new_author = Author.objects.create(
                        id = id,
                        host = host,
                        url = url,
                        displayName = displayName,
                    )

                    for friend in friends:

                        new_author.friends.add(friend)

        return data

    def updateAuthors(self):
        
        data = self.retrieveAuthors()

        #async_task(retrieveAuthors, hook = createAuthors)

    def createPosts(self,data):

        for post in data['posts']:

            try:

                ForeignPost.objects.get(id = post['id'])

            except ForeignPost.DoesNotExist:

                ForeignPost.objects.create(
                    id = post['id'],
                    author=post["author"],
                    title = post["title"],
                    source = post["source"],
                    origin = post["origin"],
                    description = post["description"],
                    visibility = post["visibility"],
                    unlisted = post["unlisted"]
                )

        # for post in task.result['posts']:

        #     # Post already exists
        #     if Post.objects.filter(id=post["id"]):
        #         continue

        #     Post.objects.create(id = post["id"],
        #                    author=post["author"],
        #                    title = post["title"],
        #                    source = post["source"],
        #                    origin = post["origin"],
        #                    description = post["description"],
        #                    content_type = post["content_type"],
        #                    visibility = post["visibility"],
        #                    unlisted = post["unlisted"],
        #     )
            # newPost = Post(id = post["id"],
            #                author=post["author"],
            #                title = post["title"],
            #                source = post["source"],
            #                origin = post["origin"],
            #                description = post["description"],
            #                content_type = post["content_type"],
            #                visibility = post["visibility"],
            #                unlisted = post["unlisted"],
            # )
            # newPost.save()

    def retrievePosts(self):

        URL = self.posts_endpoint
        location = self.name
        
        PARAMS = {
            'username': self.username,
            'password' : self.password
        }

        session = requests.Session()
        session.auth = (self.username, self.password)
        r = session.get(url= URL)
        #r = requests.get(url= URL)
        data = r.json()
        return data


    def updatePosts(self):

        data = self.retrievePosts()

        self.createPosts(data)
        #self.createPosts(data)
        #async_task(self.retrievePosts, hook = self.createPosts)