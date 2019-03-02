from django.test import TestCase
from models import author
from models.author import Author

class AuthorModelTests(TestCase):
    def setUp(self):
        pass

    def test_get_author_id(self):
        example_author = Author()
        example_id = example_author.get_author_id()
        self.assertIsNotNone(example_id)

    def test_check_if_friend(self):
        original_user = Author()
        friend = Author()
        original_user.respond_to_friend_request(friend.get_author_id(), "accept")
        self.assertIn(friend.id, original_user.friends)

    def test_check_if_not_friend(self):
        original_user = Author()
        not_friend = Author()
        original_user.respond_to_friend_request(not_friend.get_author_id(), "reject")
        self.assertNotIn(not_friend.id, original_user.friends)

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
