from Authors.models import Author
from Authors.serializers import AuthorSerializer, UserSerializer
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from Posts.models import Post, Comment
from Posts.serializers import PostSerializer
from rest_framework import status
from Tests.factory import GeneralBuilding
from urllib.parse import urlencode
from views.forms import UserCreateForm, UserLoginForm, PostTitleForm, PostInfoForm, PasswordLoginForm, SearchForm

import json 

class FrontEndTests(TestCase):

    def setUp(self):

        self.client = Client()
        self.helper_functions = GeneralBuilding()

    # Testing Front end serializers,
    # update data with a patch
    def test_author_update_displayName(self):

        pass
        
        # author = self.helper_functions.create_author()
        # author_serializer = AuthorSerializer(author)
        # old_data = author_serializer.data 
        # old_display_Name = old_data["displayName"]

        # self.client.login(username=author.user.username, password=author.user.password)

        # id = str(author.id)
        # url = "/api/authors/" + id

        # data = json.dumps( {'displayName': "newDisplayName", 'bio':"test"} )
        # response = self.client.patch(url, data=data, content_type='application/json')

        # updated_author = Author.objects.get(user=author.user)
        # new_data = AuthorSerializer(updated_author).data
        # new_Display_name = new_data["displayName"]

        # self.assertNotEqual(old_display_Name, new_Display_name)

    # Test that you can sign in.
    def test_author_sign_in(self):
        user = User.objects.create_user(username="temp_user", password="secretPass", email="email@email.com")
        user.save()
        logged_in = self.client.login(username="temp_user", password="secretPass")
        self.assertEqual(logged_in, True)

    def test_unknown_sign_in_fail(self):
    
        url = "/login/"
        data = urlencode({"username": "fake_user", "password":"not_a_real_password"})
        response = self.client.post(url, data , content_type="application/x-www-form-urlencoded")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

    # Test an author can create a post with the api
    def test_author_create_post(self):
    


        request = None # used to ignore

        author = self.helper_functions.create_author()
        self.client.login(username=author.user.username, password=author.user.password)
        post = self.helper_functions.create_post("Post_1", author)
        url = "/api/posts"

        post_id = post.id
        post_serializer = PostSerializer(post, context={'request': request})

        response = self.client.post(url, data=post_serializer.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        created_post = Post.objects.get(id= post_id)
        self.assertEqual(created_post, post)

    # Test you can signup
    def test_author_creation(self):

        user = User.objects.create(username="Bob_the_builder", password="password", email="email@email.com")
        author = Author.objects.create(user = user, displayName="Bob_the_builder")

        author= Author.objects.get(user=user)

        self.assertEqual(author.user.username, "Bob_the_builder")