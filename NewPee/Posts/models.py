from django.db import models
import json
import datetime
import uuid
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from Authors.models import Author
from NewPee import settings

# Post model represents post,
# stores an unique id, author which is a user model, title, body, image and a timestamp
class Post(models.Model):

    # override Django id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # have to change to a user model
    author = models.ForeignKey('Authors.Author', on_delete=models.CASCADE , null=True, blank=False, related_name="author")
    #author = models.CharField(max_length=140, null=False,blank=False)
    # author = models.ForeignKey(User)

    title = models.CharField(max_length=30, null=False, blank=False)
    #source = lastplaceigotthisfrom, origin = whereitcamefrom
    source = models.URLField(null=True,blank=True)
    origin = models.URLField(null=True,blank=True)
    description = models.CharField(max_length=150, default="No Description", null=False, blank=False)
    #text/markdown, text/plain, (application/base64, image/png;base64, image/jpeg;base64)???
    content_type = models.TextField(null=False,blank=False, default="text/plain")
    content = models.TextField(null=False,blank=False)
    # image = models.URLField(null=True,blank=True)
    # image = models.ImageField(upload_to = images)
    # picture = models.ImageField(upload_to = 'media/', default = 'media/None/no-img.jpg')
    post_date = models.DateTimeField(auto_now_add=True)
    #Types of visibility
    visibility_choices = (
                        ( 'PUBLIC', 'PUBLIC'),
                        ( 'FOAF', 'FOAF'),
                        ( 'PRIVATE', 'PRIVATE'),
                        ( 'SERVERONLY', 'SERVERONLY'),
                        ( 'FRIENDS', 'FRIENDS'),
    )
    visibility = models.CharField(max_length=10, choices=visibility_choices, default="PUBLIC")
    # which viewers are allowed to see it.
    visible_to = models.ManyToManyField('Authors.Author',  blank=True, related_name='visible_to')
    unlisted = models.BooleanField(default=False)

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

# class ImageModel(models.Model):
#     model_img = models.ImageField(upload_to = 'media/', default = 'media/None/no-img.jpg')


class ForeignPost(models.Model):

    # override Django id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # have to change to a user model
    #author = models.ForeignKey('Authors.Author', on_delete=models.CASCADE , null=False, blank=False, related_name="author")
    author = models.URLField(null=False, blank=False)
    # author = models.ForeignKey(User)

    title = models.CharField(max_length=30, null=False, blank=False)
    #source = lastplaceigotthisfrom, origin = whereitcamefrom
    source = models.URLField(null=True,blank=True)
    origin = models.URLField(null=True,blank=True)
    description = models.CharField(max_length=150, default="No Description", null=False, blank=False)
    #text/markdown, text/plain, (application/base64, image/png;base64, image/jpeg;base64)???
    #content_type = models.TextField(null=False,blank=False, default="text/plain")
    content = models.TextField(null=False,blank=False)
    # image = models.URLField(null=True,blank=True)
    # image = models.ImageField(upload_to = images)
    # picture = models.ImageField(upload_to = 'media/', default = 'media/None/no-img.jpg')
    post_date = models.DateTimeField(auto_now_add=True)
    #Types of visibility
    visibility_choices = (
                        ( 'PUBLIC', 'PUBLIC'),
                        ( 'FOAF', 'FOAF'),
                        ( 'PRIVATE', 'PRIVATE'),
                        ( 'SERVERONLY', 'SERVERONLY'),
                        ( 'FRIENDS', 'FRIENDS'),
    )
    visibility = models.CharField(max_length=10, choices=visibility_choices, default="PUBLIC")
    # which viewers are allowed to see it.
    #visible_to = models.ManyToManyField('Authors.Author', blank=True, related_name='visible_to')
    unlisted = models.BooleanField(default=False)
