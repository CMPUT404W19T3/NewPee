from django.test import TestCase
from .models import Author

class AuthorModelTests(TestCase):

    def test_get_author_id(self):
        test_author = Author()
        test_author_id = test_author.get_author_id()
        self.assertIsNotNone(test_author_id)

    def test_friend(self):
        friend = Author()
        has_friend = Author()
        has_friend.friends.add(friend)
        self.assertIsNotNone(has_friend.get_friends())

    def test_follow(self):
        person_to_follow = Author()
        person_following = Author()
        person_following.follow(person_to_follow)
        self.assertIsNotNone(person_following.get_following())

    def test_check_if_friend(self):
        pass
        # original_user = Author()
        # friend = Author()
        # original_user.respond_to_friend_request(friend.get_author_id(), "accept")
        # self.assertIn(friend.id, original_user.friends)

    def test_check_if_not_friend(self):
        pass
        # original_user = Author()
        # not_friend = Author()
        # original_user.respond_to_friend_request(not_friend.get_author_id(), "reject")
        # self.assertNotIn(not_friend.id, original_user.friends)

    def test_check_relationship_friend_following(self):
        pass

    def test_check_relationship_friend_not_following(self):
        pass

    def test_check_relationship_not_friend_following(self):
        pass

    def test_check_relationship_not_friend_not_following(self):
        pass

    def test_follow(self):
        pass

    def test_unfollow(self):
        pass

    def test_remove_friend(self):
        pass

    def test_change_bio(self):
        pass

    def test_add_post(self):
        pass

    def test_delete_post(self):
        pass

    def test_github_to_stream(self):
        pass
