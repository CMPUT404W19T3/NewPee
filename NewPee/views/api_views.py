from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from Authors.models import Author
from Authors.serializers import AuthorSerializer
from Posts.models import Post, Comment, ForeignPost
from Posts.serializers import PostSerializer, CommentSerializer, ForeignPostSerializer
from Authors.serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from rest_framework import permissions

from rest_framework.permissions import IsAuthenticated
from Posts.permissions import IsOwnerOrReadOnly
from Authors.permissions import IsOwnerOrReadOnlyAuthor

from itertools import chain

import collections

from django.core import serializers
import json

#https://www.django-rest-framework.org/tutorial/2-requests-and-responses/



def view_access(xpost, author):



        returnStatement = True

        post = Post.objects.get(id=xpost["id"])

        if post.unlisted == True:
            return False

        if post.visibility == "PUBLIC":
            returnStatement = True

        elif post.visibility == "PRIVATE":
            if post.privateViewAccess(author):
                returnStatement = True
            else:
                returnStatement = False



        elif post.visibility == "FRIENDS":
            if post.friendViewAccess(author):
                returnStatement = True
            else:
                returnStatement = False


        elif post.visibility == "FOAF":
            if post.FOAFViewAccess(author):
                returnStatement = True
            else:
                returnStatement = False

        elif post.visibility == "SERVER":
            if post.ServerViewAcces(author):
                returnStatement = True
            else:
                returnStatement = False




        return returnStatement









@permission_classes((IsAuthenticated,IsOwnerOrReadOnlyAuthor, ))
@api_view(['GET', 'POST'])
def Author_list(request, format=None):
    """
    List all Authors, or create an Author
    """

    #TODO: Update the context to be specific to server.
    serializer_context = {'request': request}


    if request.method == 'GET':
        Authors = Author.objects.all()
        serializer = AuthorSerializer(Authors, many=True, context=serializer_context)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE','PATCH'])
@permission_classes((IsAuthenticated,IsOwnerOrReadOnlyAuthor, ))
def Author_detail(request, pk, format= None):
    """
    Retrieve, update or delete an Author.
    """


    #TODO: Update the context to be specific to server.

    serializer_context = {'request': request}

    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author, context=serializer_context)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = AuthorSerializer(author, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((IsAuthenticated,IsOwnerOrReadOnlyAuthor, ))
@api_view(['GET', 'POST'])

def post_list(request):
    """
    List all Posts, or create anew new Post.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


    if request.method == 'GET':
        posts = Post.objects.all()
        foreignposts = ForeignPost.objects.all()

        foreignserializer = ForeignPostSerializer(foreignposts, many=True, context={'request': request})

        serializer = PostSerializer(posts, many=True, context={'request': request})


        non_visible_filtered_post = posts

        newData = []

        #print(posts)
        #print(serializer.data)

        for post in serializer.data:


            if( view_access(post, Author.objects.get(user=request.user))):
                #print(post)
                #newData.move_to_end(post)
                #print(newData)
                print("Can see", post)


            else:
                print("Can't see", post)
                #non_visible_filtered_post  = non_visible_filtered_post.filter(id=post["id"])
                non_visible_filtered_post = posts.exclude(id = post["id"])
                posts = posts & non_visible_filtered_post


                #combined = list(chain(post, combined))

        print(posts, "posts I see list")

        #newData = set(posts).difference(set(non_visible_filtered_post))
        #print(newData)

        #newData = set(posts).difference(set(newData))

        serializer2 = PostSerializer(posts, many=True, context={'request': request})



        combined = list(chain(foreignserializer.data, serializer2.data))

        combined2 = combined



        #json = serializers.serialize('json', combined)

        return Response(combined)


    elif request.method == 'POST':


        author_id = request.data["author"]

        author = AuthorSerializer( Author.objects.get(id=author_id), context={'request': request})

        request.data["author"] = author.data



        serializer = PostSerializer(data=request.data, context={'request': request})

        #serializer.initial_data["author"] = author

        if serializer.is_valid():

            print(serializer.errors)

            #print(serializer)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@login_required(login_url='/login')
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsOwnerOrReadOnly,IsAuthenticated, ))

def post_detail(request, pk):

    """
    Retrieve, update or delete a Post.

    """


    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#@permission_classes((IsAuthenticated,IsOwnerOrReadOnlyAuthor, ))
@api_view(['GET', 'POST'])
def foreignpost_list(request):

    if request.method == 'GET':
        foreignposts = ForeignPost.objects.all()
        serializer = ForeignPostSerializer(foreignposts, many=True)
        return Response(serializer.data)


    # elif request.method == 'POST':
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#@login_required(login_url='/login')
@api_view(['GET', 'POST'])
def comment_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
