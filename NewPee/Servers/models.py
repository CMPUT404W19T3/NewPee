from django.db import models
import uuid
from django_q.tasks import async_task, result
import requests
from Posts.models import Post, ForeignPost
from Authors.models import Author, ForeignAuthor

class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140, null=False, blank=False)
    host = models.URLField(max_length=200, unique=True)
    author_endpoint = models.URLField(max_length=200, unique=True)
    posts_endpoint = models.URLField(max_length=200, unique=True)





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
            'username': 'username',
            'password' : 'password'
        }

        r = requests.get(url= URL, params = PARAMS)
        data = r.json()


        ForeignPost = (data["posts"])

        for post in ForeignPost:

            foreign_author = post["author"]

            request2 = requests.get(url = foreign_author["id"] )

            data2 = request2.json()



            try:

                id = data2["id"].split("/")
                id = id[4]
                host = data2["host"]
                url = data2["url"]
                displayName = data2["displayName"]
                friends = data2["friends"]

                print(id,host,url,displayName,friends)

                new_author = Author.objects.create(
                    id = id,
                    host = host,
                    url = url,
                    displayName = displayName,
                )
                for friend in friends:
                    new_author.friends.add(friend)

            #new_author

            except:
                # already created the author
                print("failed.")

            #    pass




        return data





    def updateAuthors(self):
        
        data = self.retrieveAuthors()


        #async_task(retrieveAuthors, hook = createAuthors)




    def createPosts(self,data):

        print(data['posts'])
        
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
            'username': 'garyscary',
            'password' : '12345'
        }
        #r = requests.get(url= URL)

        #data = r.json()
        #return data


    def updatePosts(self):
        data = self.retrievePosts()
        self.createPosts(data)
        #self.createPosts(data)
        #async_task(self.retrievePosts, hook = self.createPosts)
