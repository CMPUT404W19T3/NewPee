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
from rest_framework.renderers import TemplateHTMLRenderer

# https://www.django-rest-framework.org/tutorial/3-class-based-views/

class PostList(APIView):
    """
    List all Posts, or create a new Post.
    """

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({'posts': serializer.data})


    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    """
    Retrieve, update or delete a Post.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post.html'

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
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
                return Response({'posts': post_serializer.data, 'logged_in_author':logged_in_author_serializer.data, 'comments': comment_serializer.data, 'form': form, 'comment_form': comment_form})
            except Comment.DoesNotExist:
                return Response({'posts': post_serializer.data, 'logged_in_author':logged_in_author_serializer.data, 'form': form, 'comment_form': comment_form})
