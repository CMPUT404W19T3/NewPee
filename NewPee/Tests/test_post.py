from django.test import TestCase
from Authors.models import Author
from Posts.models import Post, Comment
import datetime
import time

class PostModelTests(TestCase):
    def setUp(self):
        pass

    def test_get_post_id(self):
        test_post = Post()
        test_id = test_post.get_id()
        self.assertIsNotNone(test_id)

    def test_get_author(self):
        test_author = Author()
        test_post = Post(author=test_author)
        test_fetch_author = test_post.get_author()
        self.assertEqual(test_author, test_fetch_author)

    def test_set_image(self):
        test_post = Post()
        image_url = "https://i.ytimg.com/vi/rNxih0ikkDo/maxresdefault.jpg"
        test_post.set_image(image_url)
        # self.assertIsNotNone(test_post.get_image())
        self.assertEqual(test_post.get_image(), image_url)

    def test_post_date(self):
        test_post = Post(post_date=datetime.datetime.now())
        self.assertIsNotNone(test_post.get_post_date())

    def test_time_linear(self):
        test_post = Post(post_date=datetime.datetime.now()-datetime.timedelta(days=1))
        later_time = datetime.datetime.now()
        self.assertLess(test_post.get_post_date(), later_time)

    def test_make_private_to_me(self):
        pass

    def test_make_private_to_author(self):
        test_author = Author()
        test_post = Post(author=test_author, visibility="PRIVATE")
        self.assertEqual(test_post.visibility, "PRIVATE")
        

    def test_make_private_to_friends(self):
        pass

    def test_make_private_to_friends_of_friends(self):
        pass

    def test_make_private_to_host_friends(self):
        pass

    def test_make_public(self):
        test_author = Author()
        test_post = Post(author=test_author)
        self.assertEqual(test_post.visibility, "PUBLIC")

    def test_body_plaintext(self):
        pass

    def test_body_markdown(self):
        pass

class CommentModelTests(TestCase):
    def setUp(self):
        pass

    def test_parent(self):
        test_post = Post()
        test_comment = Comment(parent=test_post)
        self.assertEquals(test_comment.get_parent(), test_post)
