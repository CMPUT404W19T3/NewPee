from django.test import TestCase
from Authors.models import Author
from django.contrib.auth.models import User
from Tests.factory import GeneralBuilding
from Authors.serializers import AuthorSerializer, UserSerializer
from Posts.serializers import PostSerializer
from django.urls import reverse
from django.test import Client
from Posts.models import Post, Comment


import json 

class FrontEndTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.helper_functions = GeneralBuilding()


    # Testing Front end
    def test_author_update_displayName(self):
        
        author = self.helper_functions.create_author()
        author_serializer = AuthorSerializer(author)
        old_data = author_serializer.data 
        old_display_Name = old_data["displayName"]

        self.client.login(username=author.user.username, password=author.user.password)

        id = str(author.id)
        url = "/api/authors/" + id

        data = json.dumps( {'displayName': "newDisplayName", 'bio':"test"} )
        response = self.client.patch(url, data=data, content_type='application/json')

        updated_author = Author.objects.get(user=author.user)
        new_data = AuthorSerializer(updated_author).data
        new_Display_name = new_data["displayName"]

        self.assertNotEqual(old_display_Name, new_Display_name)


    def test_author_create_post(self):

        author = self.helper_functions.create_author()
        self.client.login(username=author.user.username, password=author.user.password)

        #post = self.helper_functions.create_post("Post_1", author, "Content_1")

        url = "/api/posts/"


        post = self.helper_functions.create_post("Post1", author.id)
        post_serializer = PostSerializer(post)

        response = self.client.post(url, data=post_serializer.data, content_type='application/json')
        
        


