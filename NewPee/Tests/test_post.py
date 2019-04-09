from Authors.models import Author
from Posts.models import Post, Comment
from django.test import TestCase

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

    def test_post_date(self):

        test_post = Post(post_date=datetime.datetime.now())
        
        self.assertIsNotNone(test_post.get_post_date())

    def test_time_linear(self):

        test_post = Post(post_date=datetime.datetime.now()-datetime.timedelta(days=1))
        later_time = datetime.datetime.now()

        self.assertLess(test_post.get_post_date(), later_time)

    def test_make_private_to_me(self):

        test_author = Author()
        test_post = Post(author=test_author, visibility="PRIVATE")

        self.assertEqual(test_post.visibility, "PRIVATE")
        
    def test_set_visible_to(self):
        author1 = Author()
        author2 = Author()
        author1.save()
        author2.save()
        test_post = Post(author=author1)
        #setting testpost to be visible to author2 
        test_post.set_visible_to(author2)
        test_post.save()
        self.assertEqual(test_post.visible_to.all()[0], author2)


    def test_privateViewAccess_true(self):
        author1 = Author()
        author2 = Author()
        author1.save()
        author2.save()
        test_post = Post(author=author1)
        test_post.set_visible_to(author2)
        test_post.save()
        self.assertTrue(test_post.privateViewAccess(author2))

    def test_privateViewAccess_false(self):
        author1 = Author()
        author2 = Author()
        author1.save()
        author2.save()
        test_post = Post(author=author1)
        test_post.save()
        self.assertFalse(test_post.privateViewAccess(author2))

    def test_friendViewAccess_true(self):
        author1 = Author()
        author2 = Author()
        author1.save()
        author2.save()
        author1.friends.add(author2)
        author2.friends.add(author1)
        test_post = Post(author=author1)
        test_post.save()
        self.assertTrue(test_post.friendViewAccess(author2))

    def test_friendViewAccess_false(self):
        author1 = Author()
        author2 = Author()
        author1.save()
        author2.save()
        test_post = Post(author=author1)
        test_post.save()
        self.assertFalse(test_post.friendViewAccess(author2))


    def test_FriendServerViewAcess_true(self):
        author1 = Author(host="http://newpee.herokuapp.com/")
        author2 = Author(host="http://newpee.herokuapp.com/")
        author1.save()
        author2.save()
        author1.friends.add(author2)
        author2.friends.add(author1)
        test_post = Post(author=author1)
        test_post.save()
        self.assertTrue(test_post.FriendServerViewAcess(author2))

    def test_FriendServerViewAcess_false_not_friend_same_server(self):
        author1 = Author(host="host1")
        author2 = Author(host="host1")
        author1.save()
        author2.save()
        test_post = Post(author=author1)
        test_post.save()
        self.assertFalse(test_post.FriendServerViewAcess(author2))
    
    def test_FriendServerViewAcess_false_friend_not_same_server(self):
        author1 = Author(host="host1")
        author2 = Author(host="host2")
        author1.save()
        author2.save()
        author1.friends.add(author2)
        author2.friends.add(author1)
        test_post = Post(author=author1)
        test_post.save()
        self.assertFalse(test_post.FriendServerViewAcess(author2))

    def test_FOAFViewAccess_true(self):
        author1 = Author()
        author2 = Author()
        author3 = Author()
        author1.save()
        author2.save()
        author3.save()
        #author 1 is frineds with 2 
        author1.friends.add(author2)
        author2.friends.add(author1)
        #author 2 is frineds with 3
        author2.friends.add(author3)
        author3.friends.add(author2)
        test_post = Post(author=author1)
        test_post.save()
        self.assertTrue(test_post.FOAFViewAccess(author3))

    def test_FOAFViewAccess_false(self):
        author1 = Author()
        author2 = Author()
        author3 = Author()
        author1.save()
        author2.save()
        author3.save()
        #author 1 is frineds with 2 
        author1.friends.add(author2)
        author2.friends.add(author1)
        test_post = Post(author=author1)
        test_post.save()
        self.assertFalse(test_post.FOAFViewAccess(author3))

    def test_ServerViewAcces_true(self):
        author1 = Author(host="http://newpee.herokuapp.com/")
        author2 = Author(host="http://newpee.herokuapp.com/")
        author1.save()
        author2.save()
        test_post = Post(author=author1)
        test_post.save()
        self.assertTrue(test_post.ServerViewAcces(author2))

    def test_ServerViewAcces_false(self):
        author1 = Author(host="http://newpee.herokuapp.com/")
        author2 = Author(host="testhost")
        author1.save()
        author2.save()
        test_post = Post(author=author1)
        test_post.save()
        self.assertFalse(test_post.ServerViewAcces(author2))

    def test_unlisted_false(self):
        author1 = Author(host="http://newpee.herokuapp.com/")
        author1.save()
        test_post = Post(author=author1)
        test_post.save()
        self.assertFalse(test_post.getUnlisted())

    def test_unlisted_true(self):
        author1 = Author(host="http://newpee.herokuapp.com/")
        author1.save()
        test_post = Post(author=author1, unlisted=True)
        test_post.save()
        self.assertTrue(test_post.getUnlisted())


    def test_make_public(self):

        test_author = Author()
        test_post = Post(author=test_author)

        self.assertEqual(test_post.visibility, "PUBLIC")


class CommentModelTests(TestCase):

    def setUp(self):

        pass

    def test_parent(self):

        test_post = Post()
        test_comment = Comment(parent=test_post)

        self.assertEquals(test_comment.get_parent(), test_post)