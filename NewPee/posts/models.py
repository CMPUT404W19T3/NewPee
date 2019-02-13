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
    images = ArrayField(models.URLField())
    # comments = ArrayField(models.CharField(max_length=140))


    def write_title(self,title):
        self.title = title 
        return 

    def get_title(self):
        return self.title 

    def write_body(self,body):
        self.body = body
        return

    def get_body(self):
        return self.body
    
    def add_image(self,image_url):
        self.images.append(image_url)
        return

    def get_images(self):
        return self.images

    # def add_comment(self,comment):
    #     self.comments.append(comment)
