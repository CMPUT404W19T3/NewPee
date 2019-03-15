from Authors.models import Author
from Authors.serializers import AuthorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from Posts.models import Photo  

from Posts.models import Post
from Posts.serializers import PostSerializer


class AuthorDetail(APIView):
    """
    Retrieve, update or delete an Author.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'friends.html'

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        if request.method == "GET":
            author = self.get_object(pk)
            serializer = AuthorSerializer(author)
            return Response({'author': serializer.data})

class AuthorList(APIView):
    """
    List all Authors, or create a new Author.
    """

    @csrf_exempt
    def get(self, request, format=None):
        if request.method == "GET":
            print("This is the request\n\n", request)
            authors = Author.objects.all()
            print(authors)
            author_serializer = AuthorSerializer(authors, many=True)
            posts = Post.objects.all()
            post_serializer = PostSerializer(posts, many=True)
            # print("This is a serializer: ", serializer)
            # print("This is the type: ", type(serializer))
            # print("This is the data inside of serializer", serializer.data)
            return Response({
                'authors': author_serializer.data,
                'posts': post_serializer.data,
            })


    def post(self, request, format=None):


        # # we are posting with an image, store it usign FileSystemStorage in our media folder.
        # if request.method == 'POST' and request.FILES['myfile']:


        #     myfile = request.FILES['myfile']

        #     # Future TODO: Possibly add it to the DB, but don't have too. 
        #     try:
        #         Photo.objects.create(myfile)
            
        #     except:
        #         print("Not an image!")

        #     print(myfile)
            
        #     fs = FileSystemStorage()
        #     filename = fs.save(myfile.name, myfile)
        #     uploaded_file_url = fs.url(filename)
        #     return render(request, 'homepage.html', {
        #     'uploaded_file_url': uploaded_file_url
        #     })
            


        print("Posting the authors post")

        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
