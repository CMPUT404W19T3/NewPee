from django.db import models
from django.contrib.auth.models import User
import uuid

# Author represents a user that creates posts
class Author(models.Model):


    # Using the default Django User model and adding additional features
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(max_length=500, blank=True)
    posts_created = models.PositiveIntegerField(default=0)  # correspond to a unique_id
    picture = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    friends = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", symmetrical=False, blank=True)


    # This return is inherited from Django's built-in User
    def __str__(self):
        return self.user.get_username()

    # All "get" functions for username, password, email, etc... are inherited from Django User

    def get_author_id(self):
        return self.id

    # Determine what relationship an author has with another author
    # TODO: Remove from this class

    def check_relationship(self, author_id):
        pass

    # Return all pending friend requests
    def get_friend_request(self):
        pass

    # Accept or Decline friend request based on choice
    def respond_to_friend_request(self, author_id, choice):
        pass

    # Remove an existing friend
    def remove_friend(self, author_id):
        pass

    # Follow an Author
    def follow(self, author_id):
        pass

    # Unfollow an Author
    def unfollow(self, author_id):
        pass
