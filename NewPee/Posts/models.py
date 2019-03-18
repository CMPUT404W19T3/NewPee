from django.db import models
import json
import datetime
import uuid
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField


# Post model represents post,
# stores an unique id, author which is a user model, title, body, image and a timestamp
class Post(models.Model):

    # override Django id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # have to change to a user model
    author = models.CharField(max_length=140, null=False,blank=False)
    # author = models.ForeignKey(User)

    title = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=150, default="No Description", null=False, blank=False)
    content = models.TextField(null=False,blank=False)
    image = models.URLField(null=True,blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

    # which viewers are allowed to see it.
    viewers = models.ManyToManyField(User)



    def get_id(self):
        return self.id

    def get_author(self):
        return self.author

    def get_title(self):
        return self.title

    def get_body(self):
        return self.body

    def set_image(self,image_url):
        self.image = image_url

    def get_image(self):
        return self.image

    def get_post_date(self):
        return self.post_date

#Comment class represents comment,
#stores an unique id, a parent post, author and body
class Comment(models.Model):

    # override Django id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('Post', on_delete=models.CASCADE , null=False, blank=False)
    author = models.CharField(max_length=140, null=False, blank=False)
    content = models.CharField(max_length=140, null=False, blank=False)
    post_date = models.DateTimeField(auto_now_add=True)

    def get_id(self):
        return self.id

    def get_parent(self):
        return self.parent

    def get_author(self):
        return self.author

    def get_body(self):
        return self.body

    def get_post_date(self):
        return self.post_date


'''
Possible future addon 
https://stackoverflow.com/questions/18747730/storing-images-in-db-using-django-models

'''

class Photo(models.Model):
    #
    viewers = models.ManyToManyField(User)
    photo = models.ImageField(upload_to='media/')
