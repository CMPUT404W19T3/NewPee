from Authors.models import Author
from Authors.serializers import AuthorSerializer
from datetime import datetime
from django.http import Http404
from Posts.models import Post, Comment
from Posts.serializers import PostSerializer, CommentSerializer, ForeignPostSerializer
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from views.forms import SearchForm, CommentForm

# from Posts.forms import ImageUploadForm

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

    def str_to_date_time(self, datetime_str):

        return datetime.datetime.strptime(datetime_str, '%b %d %Y %I:%M%p')

    def get(self, request, pk, *args, **kwargs):

        if request.method == "GET":

            post = self.get_object(pk)
            post_serializer = PostSerializer(post, context={'request': request})
            post_date = post.post_date
            form = SearchForm()
            comment_form = CommentForm()

            if request.user.is_anonymous:
                if (post_serializer.data["visibility"] == "PUBLIC"):
                    try:
                        comments = Comment.objects.filter(parent=pk)
                        comment_serializer = CommentSerializer(comments, many=True)
                        #if user is anooymous and comments exist
                        return Response({'posts': post_serializer.data, 'comments': comment_serializer.data, 'form': form, 'comment_form': comment_form})

                    except Comment.DoesNotExist:

                        return Response({'posts': post_serializer.data, 'form': form, 'comment_form': comment_form})

            else: 
                logged_in_author = Author.objects.get(user = request.user)
                logged_in_author_serializer = AuthorSerializer(logged_in_author, context={'request': request})

                try:

                    comments = Comment.objects.filter(parent=pk)
                    comment_serializer = CommentSerializer(comments, many=True)

                    return Response({'posts': post_serializer.data, 'logged_in_author':logged_in_author_serializer.data, 'comments': comment_serializer.data, 'form': form, 'comment_form': comment_form})

                except Comment.DoesNotExist:

                    return Response({'posts': post_serializer.data, 'logged_in_author':logged_in_author_serializer.data, 'form': form, 'comment_form': comment_form})