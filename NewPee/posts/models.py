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
    def setAuthor(self,author):
        self.author = author

    def getAuthor(self):
        return self.author

    def writeTitle(self,title):
        self.title = json.dumps(title)

    #return string 
    def getTitle(self):
        title = json.loads(self.title)
        return title 

    def writeBody(self,body):
        self.body = json.dumps(body)

    def getBody(self):
        body = json.loads(self.body)
        return body
    
    def addImage(self,image_url):
        stringImages = json.loads(self.images)
        stringImages['images'].append(image_url)
        self.images = json.dumps(stringImages)

    #returns a list of images 
    def getAllImages(self):
        stringImages = json.loads(self.images)
        images = stringImages['images']
        return images

    #return a single url for the image 
    def getImage(self,index):
        stringImages = json.loads(self.images)
        image = stringImages['images'][index]
        return image
        

    def addComment(self,username, comment):
        stringComments = json.loads(self.comments)
        commentInfo = username + ":" + comment
        stringComments['comments'].append(commentInfo)
        self.comments = json.dumps(stringComments)

    def getAllComments(self):
        stringComments = json.loads(self.comments)
        comments = stringComments['comments']
        return comments
        
    #return username and comment 
    def getComment(self,index):
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