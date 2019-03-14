from django.test import TestCase
from Posts.models import Post

class PostModelTests(TestCase):
    def setUp(self):
        pass

    def test_get_post_id(self):
        test_post = Post()
        test_id = test_post.get_id()
        self.assertIsNotNone(test_id)

    def test_get_author(self):
        test_post = Post(author="Garfield")
        test_author = test_post.get_author()
        self.assertEqual(test_author, "Garfield")

    def test_make_private_to_me(self):
        pass

    def test_make_private_to_author(self):
        pass

    def test_make_private_to_friends(self):
        pass

    def test_make_private_to_friends_of_friends(self):
        pass

    def test_make_private_to_host_friends(self):
        pass

    def test_make_public(self):
        pass

    def test_body_plaintext(self):
        pass

    def test_body_markdown(self):
        pass

class CommentModelTests(TestCase):
    def setUp(self):
        pass
