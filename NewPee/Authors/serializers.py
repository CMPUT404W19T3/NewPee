from Authors.models import Author, User
from rest_framework import serializers

# https://medium.freecodecamp.org/nested-relationships-in-serializers-for-onetoone-fields-in-django-rest-framework-bdb4720d81e6

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class AuthorSerializer(serializers.ModelSerializer):
   
    #user = UserSerializer(required=True)
  
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=15)
    bio = models.TextField(max_length=500, blank=True)
    posts_created = models.PositiveIntegerField(default=0)  # correspond to a unique_id
    picture = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    friends = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", symmetrical=False, blank=True)
    '''

    id = serializers.HyperlinkedIdentityField(view_name="api-author")
    url = serializers.HyperlinkedIdentityField(view_name="api-author")

    class Meta:

        model = Author
        fields = ('id', 'url', 'user', 'host', 'displayName', 'bio', 'posts_created', 'image', 'github_url', 'friends', 'following', 'followers')
        lookup_field = 'id'

class ForeignAuthorSerializer(serializers.ModelSerializer):

    id = serializers.HyperlinkedIdentityField(view_name="api-author")
    url = serializers.HyperlinkedIdentityField(view_name="api-author")

    class Meta:

        model = Author
        fields = ('id', 'url', 'displayName', 'bio', 'posts_created', 'picture', 'github_url', 'friends', 'following', 'followers')
        lookup_field = 'id'