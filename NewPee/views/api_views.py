from Authors.models import Author
from Authors.permissions import IsOwnerOrReadOnlyAuthor
from Authors.serializers import AuthorSerializer, UserSerializer
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
from Posts.models import Post, Comment, ForeignPost
from Posts.permissions import IsOwnerOrReadOnly
from Posts.serializers import PostSerializer, CommentSerializer, ForeignPostSerializer
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
import collections
import json

# https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
def view_access(post, author, unlisted=False):

    returnStatement = True

    print(post, post.visibility)

    # Admin can see all posts.
    if author.Admin:
        print("Author is Admin")
        return True

    if unlisted == True:
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
            
    elif post.visibility == "SERVERFRIEND":
        if post.ServerFriendsViewAcces(author):
            returnStatement = True
        else:
            returnStatement = False

    print("retuning", returnStatement)
    return returnStatement

@permission_classes((IsAuthenticated,IsOwnerOrReadOnlyAuthor, ))
@api_view(['GET', 'POST'])
def Author_list(request, format=None):

    """
    get:
        List all Authors

    post:
        Create an Author
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
    get:
        Retreieve an Author.

    put:
        Update and Author.

    delete:
        Delete and Author.
    
    patch:
        Update and Author.
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
        print("WE HAVE MADDDDDDDDDE IT")
        serializer = AuthorSerializer(author, data=request.data, partial=True, context={'request': request})
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            print("is saved")
            print(serializer.data)
            return Response(serializer.data)
        else:
            print(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsOwnerOrReadOnlyAuthor, ))
@api_view(['GET', 'POST'])
def post_list(request):
    
    """
    get:
        List all Posts.
    
    post:
        Create a new Post.
    """

    if request.user.is_anonymous:

        posts = Post.objects.filter(visibility = "PUBLIC")

        #posts.exclude(visibility != "PUBLIC")

        serializer = PostSerializer(posts, many=True, context={'request': request})

        return Response(serializer.data)

    if request.method == 'GET':

        posts = Post.objects.filter(unlisted=False)
        public_posts = Post.objects.filter(visibility="PUBLIC")
        public_posts = public_posts.exclude(unlisted=True)
        posts = posts.exclude(visibility="PUBLIC")
        serializer = PostSerializer(posts, many=True, context={'request': request})
        non_visible_filtered_post = posts

        for post in serializer.data:

            xpost = Post.objects.get(id=post["id"])

            if( view_access(xpost, Author.objects.get(user=request.user), xpost.getUnlisted())):
                pass

            else:

                non_visible_filtered_post = posts.exclude(id = post["id"])
                posts = posts & non_visible_filtered_post

        #serializer2 = PostSerializer(posts, many=True, context={'request': request})
        serializer = PostSerializer(public_posts, many=True, context={'request': request})
        serializer2 = PostSerializer(posts, many=True, context={'request': request})
        combined = list(chain(serializer.data, serializer2.data))
        #json = serializers.serialize('json', combined)
        api_response = {}
        api_response["query"] = "posts"
        api_response["posts"] = combined
        
        return Response(api_response)

    elif request.method == 'POST':

        author_id = request.data["author"]

        if("http" in author_id):

            author_id = author_id.split("/")[-1]

        unserialized_author = Author.objects.get(id=author_id)
        unserialized_author.posts_created += 1
        unserialized_author.save()
        author = AuthorSerializer(unserialized_author, context={'request': request})
        request.data["author"] = author.data
        update_vis = False

        # clean the visible to field
        if(request.data["visibility"] =="PRIVATE"):

            visible_to = request.data["visible_to"]

            try:

                other_vis_author =  Author.objects.get( displayName = request.data["other_author"])
                visible_to.append(other_vis_author)
                print("found author")

            except:

                pass

            del request.data["visible_to"]

            update_vis = True

        serializer = PostSerializer(data=request.data, context={'request': request})
        #serializer.initial_data["author"] = author

        if serializer.is_valid():

            serializer.save()

            if(update_vis):
                
                for vis_author in visible_to:
                    Post.objects.get(id=serializer.data["id"]).set_visible_to(vis_author)
            post = Post.objects.get(id=serializer.data["id"])

            #origin = 
            #source = 

            #post.update({origin:})
            #post.update({source:})
                

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@login_required(login_url='/login')
@permission_classes((IsOwnerOrReadOnly, IsOwnerOrReadOnlyAuthor))
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):

    """
    get:
        Retrieve a Post.

    put:
        Update a Post.

    delete:
        Delete a Post.
    """

    if request.user.is_anonymous:

        if request.method == 'DELETE':

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        post = Post.objects.get(pk=pk)

        if post.visibility == "PUBLIC":

            serializer = PostSerializer(post, context={'request': request})

            return Response(serializer.data)

        else:

            return Response(status=status.HTTP_401_UNAUTHORIZED)
 
    try:

        post = Post.objects.get(pk=pk)

    except Post.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)


    if( view_access(post, Author.objects.get(user=request.user))):

        pass

    else:

        return Response(status=status.HTTP_401_UNAUTHORIZED)

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

        print(request.user, "checking")

        post = Post.objects.get(pk=pk)
        author = Author.objects.get(user=request.user)

        if (author != post.author):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

#@permission_classes((IsAuthenticated,IsOwnerOrReadOnlyAuthor, ))
@api_view(['GET', 'POST'])
def foreignpost_list(request):

    """
    get:
        REEEEE

    post:
        REEEEE
    """

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
    get:
        List all comments.
    
    post:
        Create a new comment.
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

@api_view(['POST'])
def image_detail(request):

    """
    post:
        Post an image.
    """

    if request.method == 'POST' and request.FILES:
        print(request.FILES['image'])

        myfile = request.FILES['image']
            # Future TODO: Possibly add it to the DB, but don't have too.
        try:

            Photo.objects.create(myfile)

        except:

            print("Not an image!")

        print(myfile)

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        return Response(uploaded_file_url, status=status.HTTP_201_CREATED)