from django.db import models
#from users.models import Users 

# Create your models here.
class Posts(models.Model):
    #have to change to a user model
    author = models.CharField(max_length=250)
    #author = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    #have to figure out how to render markdown 
    body = models.TextField()
    #images = ArrayField(models.URLField())
    # comments = ArrayField(models.CharField(max_length=140))


    def writeTitle(self,title):
        self.title = title 
        return 

    def getTitle(self):
        return self.title 

    def writeBody(self,body):
        self.body = body
        return

    def getBody(self):
        return self.body
    
    def addImage(self,image_url):
        self.images.append(image_url)
        return

    def getImages(self):
        return self.images

    # def add_comment(self,comment):
    #     self.comments.append(comment)
