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



    def retrieveAuthors(self,data):
        foreign_posts = (data["posts"])

        for post in foreign_posts:

            foreign_author = post["author"]
            foreign_author_uuid = foreign_author["id"].split("/")[-1]


            try:

                Authors.models.Author.objects.get(id = foreign_author_uuid)

            except Authors.models.Author.DoesNotExist:




                #author_uuid = foreign_author["id"]
                author_url =  foreign_author["url"]
                author_host =  foreign_author["host"]
                author_displayName =  foreign_author["displayName"]

                new_author = Authors.models.Author.objects.create(
                        id =  foreign_author_uuid,
                        host = author_host,
                        url = author_url,
                        displayName = author_displayName,
                    )

                #for friend in friends:

                #    new_author.friends.add(friend)
                print("\n\n\n\ CREATED AUTHOR \n\n\n")


                PARAMS = {
                'username': self.username,
                'password' : self.password
                }

                session = requests.Session()
                session.auth = (self.username, self.password)



                # Can't pull data from other servers, only pull others server data from our authorized host
                try:
                    if(self.host not in foreign_author["id"]):
                        url = self.author_endpoint + foreign_author_uuid
                    else:
                        url = foreign_author["id"]



                    request2 = session.get(url = url)
                    data2 = request2.json()


                    friends = data2["friends"]


                    new_author.displayName = data2["displayName"]

                    try:
                        new_author.firstname = data2["firstName"]
                        new_author.lastname = data2["lastName"]
                    except:
                        pass # Their server doesn't include lastname, firstname
                        
                #their server doesn't have author end points
                except:
                    pass


        return data

    def updateAuthors(self,data):

        data = self.retrieveAuthors(data)

        #async_task(retrieveAuthors, hook = createAuthors)

    def createPosts(self,data):

        for post in data['posts']:

            self.updateAuthors(data)


            try:

                db_post = Posts.models.Post.objects.get(id = post['id'])


            except :

                try:
                    foreign_author = Authors.models.Author.objects.get(url = post["author"]["id"])
                    Posts.models.Post.objects.create(
                        id = post['id'],
                        author=foreign_author,
                        title = post["title"],
                        source = post["source"],
                        origin = post["origin"],
                        description = post["description"],
                        visibility = post["visibility"],
                        unlisted = post["unlisted"]
                    )
                # post belongs to another site we don't affiliate with.
                except:
                    pass






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

        #self.isActive = False # Already retrieved data

        #print(self.isActive)
        #self.save()
