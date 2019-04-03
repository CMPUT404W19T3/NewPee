from django.db import models
from django.contrib.auth.models import User
import uuid

# Author represents a user that creates posts
class Author(models.Model):

    # Using the default Django User model and adding additional features
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(null=True,blank=True)
    host = models.URLField(default="newpee.herokuapp.com/")
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    displayName = models.CharField(max_length=15)
    bio = models.TextField(max_length=500, blank=True)
    posts_created = models.PositiveIntegerField(default=0)  # correspond to a unique_id
    # picture = models.URLField(blank=True)
    image = models.ImageField(upload_to="profile_image", blank=True, default='NewPee.png')
    github_url = models.URLField(blank=True)

    friends = models.ManyToManyField("self", related_name="_friends", blank=True)
    following = models.ManyToManyField("self", related_name="_following", symmetrical=False, blank=True)
    followers = models.ManyToManyField("self", related_name="_followers", symmetrical=False, blank=True)
    friend_requests = models.ManyToManyField("self", related_name="_friend_requests", symmetrical=False, blank=True)


    # Only Admin can Change.
    isAuthorized = models.BooleanField(default=True)

    # This return is inherited from Django's built-in User
    def __str__(self):

        try:
            return self.user.get_username()
        except:
            return self.displayName


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

    # we have recieved a friend request from the author
    def send_friend_request(self, author):

        self.followers.add(author)
        self.friend_requests.add(author)


        # if we are following the author add him to our friends.
        if (author in self.following.all()):

            self.friends.add(author)
            self.friend_requests.remove(author)

        self.save()
    
    # Accept or Decline friend request based on choice
    def respond_to_friend_request(self, author, choice):

        self.friend_requests.remove(author) # no longer in our friend requests either way.
            
        if( choice == "accept"):
            self.friends.add(author)
            self.follow(author)
            
        self.save()

    # Remove an existing friend
    def remove_friend(self):
        self.friends.remove(author)



#TODO: FIX 


class ForeignAuthor(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=1000, null=True,blank=True)
    host = models.URLField(default="newpee.herokuapp.com/")

    displayName = models.CharField(max_length=15)
    bio = models.TextField(max_length=500, blank=True)
    posts_created = models.PositiveIntegerField(default=0)  # correspond to a unique_id
    picture = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    friends = models.ManyToManyField(Author, related_name="_friendsForeign", blank=True)
    following = models.ManyToManyField(Author, related_name="_followingForeign", symmetrical=False, blank=True)
    followers = models.ManyToManyField(Author, related_name="_followersForeign", symmetrical=False, blank=True)
    friend_requests = models.ManyToManyField(Author, related_name="_friend_requestsForeign", symmetrical=False, blank=True)


    # Only Admin can Change.
    isAuthorized = models.BooleanField(default=True)


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

    # we have recieved a friend request from the author
    def send_friend_request(self, author):

        self.followers.add(author)
        self.friend_requests.add(author)


        # if we are following the author add him to our friends.
        if (author in self.following.all()):

            self.friends.add(author)
            self.friend_requests.remove(author)

        self.save()
    
    # Accept or Decline friend request based on choice
    def respond_to_friend_request(self, author, choice):

        self.friend_requests.remove(author) # no longer in our friend requests either way.
            
        if( choice == "accept"):
            self.friends.add(author)
            self.follow(author)
            
        self.save()

    # Remove an existing friend
    def remove_friend(self):
        self.friends.remove(author)
