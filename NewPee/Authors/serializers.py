from rest_framework import serializers
from Authors.models import Author



class AuthorSerializer(serializers.ModelSerializer):
   
  
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(max_length=500, blank=True)
    posts_created = models.PositiveIntegerField(default=0)  # correspond to a unique_id
    picture = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    friends = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", symmetrical=False, blank=True)
    '''


    class Meta:
        model = Author
        fields = ('id', 'user', 'bio', 'posts_created', 'picture', 'github_url', 'friends', 'following', 'followers')
        lookup_field = 'id'

