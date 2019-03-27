from rest_framework import serializers
from Posts.models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey('Authors.Author', on_delete=models.CASCADE , null=False, blank=False, related_name="author")
    title = models.CharField(max_length=30, null=False, blank=False)
    source = models.URLField(null=True,blank=True)
    origin = models.URLField(null=True,blank=True)
    description = models.CharField(max_length=150, null=False, blank=False)
    content_type = models.TextField(null=False,blank=False, default="text/plain")
    content = models.TextField(null=False, blank=False)
    image = models.URLField(null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    visibility_choices = (
                        ( 'PUBLIC', 'PUBLIC'),
                        ( 'FOAF', 'FOAF'),
                        ( 'PRIVATE', 'PRIVATE'),
                        ( 'SERVERONLY', 'SERVERONLY'),
                        ( 'FRIENDS', 'FRIENDS'),
    )
    visibility = models.CharField(max_length=10, choices=visibility_choices, default="PUBLIC")
    visible_to = models.ManyToManyField('Authors.Author', blank=True, related_name='visible_to')
    unlisted = models.BooleanField(default=False)
    """

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'source', 'origin', 'description', 'content', 'content_type', 'post_date', 'visibility', 'visible_to', 'unlisted')
        lookup_field = 'id'

class CommentSerializer(serializers.ModelSerializer):
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('Post', on_delete=models.CASCADE , null=False,blank=False)
    author = models.CharField(max_length=25, null=False,blank=False)
    content = models.CharField(max_length=140, null=False,blank=False)
    post_date = models.DateTimeField(auto_now_add=True)
    """

    class Meta:
        model = Comment
        fields = ('id', 'parent', 'author', 'content', 'post_date', )