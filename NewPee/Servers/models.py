from django.db import models
import uuid
from django_q.tasks import async_task, result
import requests
from Posts.models import Post

class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140, null=False, blank=False)
    host = models.URLField(max_length=200, unique=True)
    author_endpoint = models.URLField(max_length=200, unique=True)
    posts_endpoint = models.URLField(max_length=200, unique=True)





    def createAuthors(task):


        for authors in task.result['authors']:

            author_uuid = authors["id"]
            firstname = authors["firstname"]
            lastname = authors["lastname"]
            email= authors["email"]

            if ( Author.objects.filter(id=author_uuid)):
                pass




    def retrieveAuthors():

        URL = self.authors_endpoint

        location = self.name

        PARAMS = {
            'username': 'username',
            'password' : 'password'
        }

        r = requests.get(url= URL, params = PARAMS)
        data = r.json()

        return data





    def updateAuthors():

        async_task(retrieveAuthors, hook = createAuthors)




    def createPosts(self,task):





        for post in task.result['posts']:

            # Post already exists
            if Post.objects.filer(id=post["id"]):
                continue



            newPost = Post(id = post["id"],
                           author=post["author"],
                           title = post["title"],
                           source = post["source"],
                           origin = post["origin"],
                           description = post["description"],
                           content_type = post["content_type"],
                           visibility = post["visibility"],
                           unlisted = post["unlisted"],
            )
            newPost.save()





    def retrievePosts(self):
        URL = self.posts_endpoint
        location = self.name
        
        PARAMS = {
            'username': 'garyscary',
            'password' : '12345'
        }
        r = requests.get(url= URL)

        data = r.json()
        print(data)



    def updatePosts(self):
        self.retrievePosts()

        #async_task(self.retrievePosts, hook = self.createPosts)
