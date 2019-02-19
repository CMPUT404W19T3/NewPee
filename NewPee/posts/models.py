from django.db import models
from django.contrib.postgres.fields import JSONField
import json
import datetime

# Create your models here.
class Posts(models.Model):
    #have to change to a user model
    author = JSONField()
    #author = models.ForeignKey(User)

    title = JSONField()
    #have to figure out how to render markdown
    body = JSONField()


    #will be stored as '{"images":[url1, url2,...]}'
    images = JSONField()

    #"{comments:[user1:comment1, user2:comment2,...]}""
    comments = JSONField()

    #'{"like":0, "dislike":0}'
    votes = JSONField()
    timestamp = json.dumps(str(datetime.datetime.now()))
    
    def __init__(self):
        self.images = json.dumps({"images":[]})
        self.comments = json.dumps({"comments":[]})
        self.votes = json.dumps({"like": 0, "dislike": 0})


    #pass in author object in json 
    def set_author(self,author):
        self.author = author

    def get_author(self):
        return self.author

    def write_title(self,title):
        self.title = json.dumps(title)

    #return string 
    def get_title(self):
        title = json.loads(self.title)
        return title 

    def write_body(self,body):
        self.body = json.dumps(body)

    def get_body(self):
        body = json.loads(self.body)
        return body
    
    def add_image(self,image_url):
        stringImages = json.loads(self.images)
        stringImages['images'].append(image_url)
        self.images = json.dumps(stringImages)

    #returns a list of images 
    def get_all_images(self):
        stringImages = json.loads(self.images)
        images = stringImages['images']
        return images

    #return a single url for the image 
    def get_image(self,index):
        stringImages = json.loads(self.images)
        image = stringImages['images'][index]
        return image
        

    def add_comment(self,username, comment):
        stringComments = json.loads(self.comments)
        commentInfo = username + ":" + comment
        stringComments['comments'].append(commentInfo)
        self.comments = json.dumps(stringComments)

    def get_all_comments(self):
        stringComments = json.loads(self.comments)
        comments = stringComments['comments']
        return comments
        
    #return username and comment 
    def get_comment(self,index):
        stringComments = json.loads(self.comments)
        comment = stringComments['comments'][index]
        username = comment.split(":")[0]
        commentText = comment.split(":")[1]
        return username, commentText

    def like(self):
        stringVotes = json.loads(self.votes)
        likes = stringVotes['like']
        likes += 1 
        stringVotes['like'] = likes
        self.votes = json.dumps(stringVotes)

    def dislike(self):
        stringVotes = json.loads(self.votes)
        dislikes = stringVotes['dislike']
        dislikes += 1 
        stringVotes['dislike'] = dislikes
        self.votes = json.dumps(stringVotes)