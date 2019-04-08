from Authors.models import Author, User
from Authors.serializers import AuthorSerializer, UserSerializer
from Posts.models import Post, Comment, ForeignPost
from rest_framework import serializers

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
    published = models.DateTimeField(auto_now_add=True)
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

    author = AuthorSerializer(many=False, read_only=True, )

    class Meta:

        model = Post
        fields = ('id', 'author', 'title', 'source', 'origin', 'description', 'content', 'contentType', 'published', 'visibility', 'visible_to', 'unlisted')
        lookup_field = 'id'

    # custom save method to work with visible_To
    '''
    def save(self,visible_to):

        print(self.validated_data)

        try:

            id =  self.validated_data['id']
            author =  self.validated_data['author']
            title =  self.validated_data['title']
            source =  self.validated_data ['source']
            origin =  self.validated_data ['origin']
            description =  self.validated_data ['description']
            content =  self.validated_data ['content']
            content_type =  self.validated_data['content_type'] 
            post_date =  self.validated_data ['post_date']
            visibility =  self.validated_data ['visibility']
            #visible_to.set(visible_to)
            unlisted =  self.validated_data ['unlisted']

        except:
            
            pass
    '''

    def create(self, validated_data):

        #print(self.validated_data)
        #print(validated_data, "?")
        #author = Author.objects.get(id = validated_data["author"])
        #validated_data["author"] = author

        return Post.objects.create(**validated_data)

    def to_internal_value(self, data):

        #print('\n')
        #print(data, "\n")
        internal_value = super(PostSerializer, self).to_internal_value(data)
        author = data.get("author")
        stripped_id = author["id"].split("/",5)
        author_object = Author.objects.get( id= stripped_id[5])
        internal_value.update({"author":author_object})

        #my_non_model_field_value = ConvertRawValueInSomeCleverWay(my_non_model_field_raw_value)
        #internal_value.update({"my_non_model_field": my_non_model_field_value})

        print("Post serializer finished")

        return internal_value


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

class ForeignPostSerializer(serializers.ModelSerializer):

    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.URLField(null=False, blank=False)
    title = models.CharField(max_length=30, null=False, blank=False)
    source = models.URLField(null=True,blank=True)
    origin = models.URLField(null=True,blank=True)
    description = models.CharField(max_length=150, default="No Description", null=False, blank=False)
    content = models.TextField(null=False,blank=False)
     = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, choices=visibility_choices, default="PUBLIC")
    unlisted = models.BooleanField(default=False)
    '''

    #author = AuthorSerializer(many=False, read_only=True, )

    class Meta:

        model = ForeignPost
        fields = ('id', 'author', 'title', 'source', 'origin', 'description', 'content', '', 'visibility', 'unlisted')
        lookup_field = 'id'

    # def create(self, validated_data):

    #     #print(self.validated_data)
    #     #print(validated_data, "?")
    #     #author = Author.objects.get(id = validated_data["author"])
    #     #validated_data["author"] = author

    #     return ForeignPost.objects.create(**validated_data)

    # def to_internal_value(self, data):
    
    #     #print('\n')
    #     #print(data, "\n")
    #     internal_value = super(ForeignPostSerializer, self).to_internal_value(data)
    #     author = data.get("author")
    #     stripped_id = author["id"].split("/",5)
    #     print(stripped_id[5])
    #     author_object = Author.objects.get( id= stripped_id[5])

    #     print(author_object, "???")

    #     internal_value.update({"author":author_object})
    #     #my_non_model_field_value = ConvertRawValueInSomeCleverWay(my_non_model_field_raw_value)
    #     #internal_value.update({"my_non_model_field": my_non_model_field_value})
    #     print("finished")
    #     return internal_value 