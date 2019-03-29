from Authors.models import Author
from Authors.serializers import AuthorSerializer
from Posts.models import Post, Comment
from Authors.models import Author
from Posts.serializers import PostSerializer, CommentSerializer
from Authors.serializers import AuthorSerializer
from views.forms import SearchForm, CommentForm
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_swagger import renderers


from rest_framework import status , generics

# https://www.django-rest-framework.org/tutorial/3-class-based-views/

# class SwaggerSchemaView(APIView):

#     permission_classes = [AllowAny]
#     renderer_classes = [
#         renderers.OpenAPIRenderer,
#         renderers.SwaggerUIRenderer
#     ]

class PostList(APIView):

    """
    Resource for managing all posts (PostList).
    ---
    get:
        parameters_strategy:
            form: replace
        parameters:
        - id: string
          author: name
          title: string
          source:
          origin:
          content:
          content_type: application/json
          post_date: 
          visibility:
          visible_to:
          unlisted:
    
    post:
        omit_serializer: true
        parameters_strategy:
            form: replace
        parameters:
        - id: string
          author: name
          title:
          source:
          origin:
          content:
          content_type:
          post_date:
          visibility:
          visible_to:
          unlisted:
    """

    serializer_class = PostSerializer
    model = Post
    queryset = Post.objects.all()

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'

    def get(self, request, format=None):

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({'posts': serializer.data})

    def post(self, request, format=None):

        """
        description: Create Posts.
        """

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):

    """
    Retrieve, update or delete a Post (PostDetail).
    ---
    get_object:
        parameters_strategy:
            form: replace
        parameters:
        - id: string
          author: name
          title: string
          source:
          origin:
          content:
          content_type: application/json
          post_date: 
          visibility:
          visible_to:
          unlisted:
    
    get:
        omit_serializer: true
        parameters_strategy:
            form: replace
        Parameters:
        - id: string
          author: name
          title:
          source:
          origin:
          content:
          content_type:
          post_date:
          visibility:
          visible_to:
          unlisted:
    """

    serializer_class = PostSerializer
    model = Post
    queryset = Post.objects.all()

    def get_object(self, pk):

        """
        View all existent posts.
        """

        try:

            return Post.objects.get(pk=pk)

        except Post.DoesNotExist:

            raise Http404

    def get(self, request, pk, *args, **kwargs):

        """
        View post and its details if existent.
        """

        if request.method == "GET":

            post = self.get_object(pk)
            post_serializer = PostSerializer(post)

            logged_in_author = Author.objects.get(user = request.user)
            logged_in_author_serializer = AuthorSerializer(logged_in_author)

            form = SearchForm()

            comment_form = CommentForm()

            try:

                comments = Comment.objects.filter(parent=pk)
                comment_serializer = CommentSerializer(comments, many=True)

                return Response({'posts': post_serializer.data, 'author':logged_in_author_serializer.data, 'comments': comment_serializer.data, 'form': form, 'comment_form': comment_form})

            except Comment.DoesNotExist:

                return Response({'posts': post_serializer.data, 'author':logged_in_author_serializer.data, 'form': form, 'comment_form': comment_form})

    # For Image Uploading
    # def upload_image(self, request):
    #     if request.method == "POST":
    #         form = ImageUploadForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save()
    #             return HttpResponse('/success/url/')
    #         else:
    #             form = ImageUploadForm
    #             return render(request, 'home.html', {'form': form})