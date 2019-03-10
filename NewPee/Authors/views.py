from django.shortcuts import render


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Authors.models import Author
from Authors.serializers import AuthorSerializer


#https://www.django-rest-framework.org/tutorial/2-requests-and-responses/


@api_view(['GET', 'POST'])
def Author_list(request, format=None):
    """
    List all Authors, or create an Author

    """

    if request.method == 'GET':
        Authors = Author.objects.all()
        serializer = AuthorSerializer(Authors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def Author_detail(request, pk, format= None):
    """
    Retrieve, update or delete an Author.
    """
    try:
        Author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(Author)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AuthorSerializer(Author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)