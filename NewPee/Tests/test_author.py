from Authors.models import Author
from Authors.serializers import AuthorSerializer, UserSerializer
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from Tests.factory import GeneralBuilding
from django.db.models.query import EmptyQuerySet

import json

class AuthorModelTests(TestCase):

    def setUp(self):

        self.client = Client()
        self.helper_functions = GeneralBuilding()

    def test_get_author_id(self):

        test_author = Author()
        test_author_id = test_author.get_author_id()

        self.assertIsNotNone(test_author_id)

    def test_distinct_ids(self):

        author_1 = Author()
        author_2 = Author()

        self.assertNotEqual(author_1.get_author_id(), author_2.get_author_id())



    def test_follow(self):
        #create two author object
        person_to_follow = Author()
        person_to_follow.save()
        person_following = Author()
        person_following.save()
        #call follow
        person_following.follow(person_to_follow)
        #assert person_to_follow and first element(there is only one) of person_following's following list
        self.assertEqual(person_following.following.all()[0], person_to_follow)

    def test_followed(self):
        #create two author object
        person_to_follow = Author()
        person_to_follow.save()
        person_following = Author()
        person_following.save()
        #call follow
        person_following.followed(person_to_follow)
        #assert person_to_follow and first element(there is only one) of person_following's followers list
        self.assertEqual(person_following.followers.all()[0], person_to_follow)

    def test_unfollow(self):
        #create two author object
        person_to_follow = Author()
        person_to_follow.save()
        person_following = Author()
        person_following.save()
        #call follow
        person_following.follow(person_to_follow)
        #assert person_to_follow and first element(there is only one) of person_following's following list
        self.assertEqual(person_following.following.all()[0], person_to_follow)
        person_following.unfollow(person_to_follow)
        #assert if the the following list is empty
        self.assertQuerysetEqual(person_following.following.all(), person_following.following.none())

    def test_get_following(self):
        #create two author object
        person_to_follow = Author()
        person_to_follow.save()
        person_following = Author()
        person_following.save()
        self.assertQuerysetEqual(person_following.following.all(), person_following.following.none())
        person_following.follow(person_to_follow)
        following = person_following.get_following()
        self.assertEqual(following[0], person_to_follow)


    def test_add_friend_request(self):
        author1 = Author()
        author1.save()
        author2 = Author()
        author2.save()
        author1.add_friend_request(author2)
        requests = author1.friend_requests.all()
        self.assertEqual(requests[0], author2)



    def test_check_if_friend(self):

        original_user = self.helper_functions.create_author()
        friend = self.helper_functions.create_author(username="temp_user2")

        original_user.follow(friend)
        friend.follow(original_user)
        original_user.respond_to_friend_request(friend.get_author_id(), "accept")


    def test_check_if_not_friend(self):

        original_user = self.helper_functions.create_author()
        not_friend = self.helper_functions.create_author(username="temp_user2")

        original_user.respond_to_friend_request(not_friend.get_author_id(), "reject")
        self.assertNotIn(not_friend.id, original_user.friends.all())


    def test_remove_friend(self):
        author1 = Author()
        author2 = Author()
        author1.friends.add(author2)
        author1.save()
        author2.save()
        self.assertEqual(author1.friends.all()[0], author2)
        author1.remove_friend(author2)
        self.assertQuerysetEqual(author1.friends.all(), author1.friends.none())
