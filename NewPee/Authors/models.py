from django.db import models
from django.contrib.auth.models import User
import uuid

# Author represents a user that creates posts
class Author(models.Model):

    # Using the default Django User model and adding additional features
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(null=True,blank=True)
    host = models.URLField(default="newpee.herokuapp.com/")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=15)
    bio = models.TextField(max_length=500, blank=True)
    posts_created = models.PositiveIntegerField(default=0)  # correspond to a unique_id
    picture = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    friends = models.ManyToManyField("self", related_name="_friends", blank=True)
    following = models.ManyToManyField("self", related_name="_following", symmetrical=False, blank=True)
    followers = models.ManyToManyField("self", related_name="_followers", symmetrical=False, blank=True)
    friend_requests = models.ManyToManyField("self", related_name="_friend_requests", symmetrical=False, blank=True)




    # This return is inherited from Django's built-in User
    def __str__(self):
        return self.user.get_username()

    # All "get" functions for username, password, email, etc... are inherited from Django User

    def get_author_id(self):
        return self.id

    # Determine what relationship an author has with another author
    # TODO: Remove from this class

    def is_friend(self, author_id):
        """
        Check if an author is a friend.
        """


        friends_ids = self.friends.all().values('id')

        try:
            if(friends_ids.get(id=author_id)):
                return True
        except:
            return False



        #return self.friends.filter(uuid=author_id).exists()

    def get_friend_models(self):
        return self.friends

    def get_friends(self):
        """
        Returns all local friends.
        """
        return self.friends.all()

    def follow(self, author):
        """
        Follow local author.
        """
        self.following.add(author)
        self.save()


    def followed(self,author):
        self.followers.add(author)
        self.save()

    def unfollow(self, author):
        """
        Unfollow local author.
        """
        self.following.remove(author)
        self.save()
    
    def get_following(self):
        """
        Return all authors that the current author is following.
        """
        return self.following.all()

    # Return all pending friend requests
    def get_friend_request(self):
        return self.friend_requests.all()
        

    def send_friend_request(self, author):

        self.followed(author)
        self.friend_requests.add(author)
        self.save()


    
    # Accept or Decline friend request based on choice
    def respond_to_friend_request(self, author, choice):

        self.friend_requests.remove(author) # no longer in our friend requests either way.
            
        if( choice == "accept"):
            self.friends.add(author)
            self.follow(author)

        self.save()

        

    # Remove an existing friend
    def remove_friend(self, author_id):
        pass
