from rest_framework import serializers
from Posts.models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(max_length=25, null=False, blank=False)
    title = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=150, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    image = models.URLField(null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    """

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'description', 'content', 'image', 'post_date')


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
        fields = ('id', 'parent', 'author', 'content', 'post_date')