from Authors.models import Author
from Authors.serializers import AuthorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.decorators.csrf import csrf_exempt


class AuthorList(APIView):
    """
    List all Authors, or create a new Author.
    """
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'homepage.html'

    @csrf_exempt
    def get(self, request, format=None):

        if request.method == "POST":
            return HttpResponse("Hello, world.")



        if request.method == "GET":
            print("This is the request\n\n", request)
            author = Author.objects.all()
            serializer = AuthorSerializer(author, many=True)
            # print("This is a serializer: ", serializer)
            # print("This is the type: ", type(serializer))
            # print("This is the data inside of serializer", serializer.data)
            return Response({'authors': serializer.data})


    def post(self, request, format=None):

        print("Posting the authors post")

        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
