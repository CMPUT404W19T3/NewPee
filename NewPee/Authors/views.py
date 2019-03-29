from Authors.models import Author
from Authors.serializers import AuthorSerializer
from django.http import Http404, HttpResponseRedirect
from views.forms import SearchForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from Posts.models import Photo  
from Authors import models
from Posts.models import Post
from Posts.serializers import PostSerializer

from rest_framework.generics import ListAPIView
from collections import OrderedDict
import yaml

from rest_framework.decorators import action
from django.views.generic import RedirectView

class AuthorDetail(APIView):

    fields = ('id', 'user', 'displayName', 'bio', 'posts_created', 'picture', 'github_url', 'friends', 'following', 'followers')

    """
    Retrieve, update or delete an Author.
    ---
    get_object:
        parameters_strategy:
            form: replace
        parameters:
            - id: uuid
              user: name
              displayName:
              bio:
              posts_created: number
              github_url: string
              friends: list
              following: list
              followers: list
    get:
        parameters_strategy:
            form: replace
        parameters:
            - id: uuid
              user: name
              displayName:
              bio:
              posts_created: number
              github_url: string
              friends: list
              following: list
              followers: list
    post:
        parameters_strategy:
            form: replace
        parameters:
            - id: uuid
              user: name
              displayName:
              bio:
              posts_created: number
              github_url: string
              friends: list
              following: list
              followers: list
    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'

    serializer_class = AuthorSerializer
    model = Author
    queryset = Author.objects.all()

    def get_object(self, pk):

        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):

        """
        title:
        Return the current author.
        """

        if request.method == "GET":
            author = self.get_object(pk)
            author_serializer = AuthorSerializer(author)

            logged_in_author = Author.objects.get(user = request.user)
            logged_in_author_serializer = AuthorSerializer(logged_in_author)

            form = SearchForm()
            #print("\n\nSEARCH:", request.GET.get('search'))
            search = request.GET.get('search')
            
            if search:
                authors = Author.objects.filter(displayName__icontains = search)
                print("This is the authors", authors)
                return Response({'authors': authors, 'form': form, 'search': search}, template_name='search.html')

            try:
                posts = Post.objects.filter(author=pk)
                post_serializer = PostSerializer(posts, many=True)
                print("Hello", post_serializer.data)
                return Response({'author': author_serializer.data, 'posts': post_serializer.data, \
                'form': form, 'logged_in_author':logged_in_author_serializer.data})

            except Post.DoesNotExist:
                return Response({'author': author_serializer.data, 'form': form})

    # Clean Up After
    def post(self, request, pk, *args, **kwargs):

        print(">")
        if request.method == 'POST' and request.FILES['myfile']:

            author = self.get_object(pk)
            author_serializer = AuthorSerializer(author)
            logged_in_author = Author.objects.get(user = request.user)
            logged_in_author_serializer = AuthorSerializer(logged_in_author)
            
            form = SearchForm()
            search = request.GET.get('search')

            myfile = request.FILES['myfile']

            # Future TODO: Possibly add it to the DB, but don't have too. 
            try:
                Photo.objects.create(myfile)
            
            except:
                print("Not an image!")

            print(myfile)
            
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            #return redirect('/authors',  uploaded_file_url= uploaded_file_url)

            try:
                posts = Post.objects.filter(author=pk)
                post_serializer = PostSerializer(posts, many=True)

                return render(request, 'home.html', {
                'uploaded_file_url': uploaded_file_url, \
                'author': author_serializer.data, 'posts': post_serializer.data, \
                'form': form, 'logged_in_author':logged_in_author_serializer.data })
            except:
                 return render(request, 'home.html', {
                'uploaded_file_url': uploaded_file_url, \
                'author': author_serializer.data,  \
                'form': form, 'logged_in_author':logged_in_author_serializer.data })

class AuthorList(APIView):
    """
    List all Authors, or create a new Author.
    ---
    get:
        parameters_strategy:
            form: replace
        parameters:
            - id: uuid
              user: name
              displayName:
              bio:
              posts_created: number
              github_url: string
              friends: list
              following: list
              followers: list
    post:
        parameters_strategy:
            form: replace
        parameters:
            - id: uuid
              user: name
              displayName:
              bio:
              posts_created: number
              github_url: string
              friends: list
              following: list
              followers: list
    """

    serializer_class = AuthorSerializer
    model = Author
    queryset = Author.objects.all()

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

        # we are posting with an image, store it usign FileSystemStorage in our media folder.
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

'''
a reponse if friends or not
ask a service GET http://service/author/<authorid>/friends/
responds with:
{
	"query":"friends",
	# Array of Author UUIDs
	"authors":[
		"http://host3/author/de305d54-75b4-431b-adb2-eb6b9e546013",
		"http://host2/author/ae345d54-75b4-431b-adb2-fb6b9e547891"
	]
}

# ask a service if anyone in the list is a friend
# POST to http://service/author/<authorid>/friends
{
	"query":"friends",
	"author":"<authorid>",
	# Array of Author ids
	"authors": [
	    "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
		"http://127.0.0.1:5454/author/ae345d54-75b4-431b-adb2-fb6b9e547891",
		"...",
		"...",
		"..."
  	]
}

# reponds with
{
	"query":"friends",
 	"author":"<authorid>", # where <authorid> is the full URL of the author in question
 	# Array of Author ids who are friends
	"authors": [
	    "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
		"http://127.0.0.1:5454/author/ae345d54-75b4-431b-adb2-fb6b9e547891",
		"..."
  	]
}

'''

class AuthorfriendsView(APIView):

    """
    List of Author's friends.
    ---
    get:
        parameters_strategy:
            form: replace
        parameters:
            - id: uuid
              user: name
              displayName:
              bio:
              posts_created: number
              github_url: string
              friends: list
              following: list
              followers: list
    post:
        parameters_strategy:
            form: replace
        parameters:
            - id: uuid
              user: name
              displayName:
              bio:
              posts_created: number
              github_url: string
              friends: list
              following: list
              followers: list
    """

    serializer_class = AuthorSerializer
    model = Author
    queryset = Author.objects.all()

    @csrf_exempt
    def get(self, request, pk, *args, **kwargs):

            author = get_object_or_404(models.Author, id= pk)

            response_data = OrderedDict()
            response_data['query'] = 'friends'
            response_data['authors'] = author.get_friends().values('id')

            return Response(response_data)

    @csrf_exempt
    def post(self, request, pk, *args, **kwargs):

            author = get_object_or_404(models.Author, id= pk)
             
            try:
                authors = request.data["authors"]

                friends = []

                for request_author in authors:

                    print(request_author)
                    our_friends = author.get_friends().values('id')
                    print(our_friends)

                    try:
                        if our_friends.get(id=request_author):
                            print("appending author")
                            friends.append(request_author)
                    except:
                        pass

                response_data = OrderedDict()
                response_data['query'] = 'friends'
                response_data['author'] = author.id
                response_data['authors'] = friends

                return Response(response_data)

            except:

                return Response(status=status.HTTP_400_BAD_REQUEST)

# Return a boolean for if two authors are friends
class AuthorIsfriendsView(APIView):

    """
    List all Authors, or create a new Author.
    ---
    get:
        parameters_strategy:
            form: replace
        parameters:
            - id: uuid
              user: name
              displayName:
              bio:
              posts_created: number
              github_url: string
              friends: list
              following: list
              followers: list
    """

    serializer_class = AuthorSerializer
    model = Author
    queryset = Author.objects.all()

    @csrf_exempt
    def get(self, request, pk, pk2, *args, **kwargs):

        author = get_object_or_404(models.Author, id= pk)
        author2 = get_object_or_404(models.Author, id= pk2)

        print(AuthorSerializer(author).data)

        friends_bool = False

        if author.is_friend(author2.id) and author2.is_friend(author.id):
            friends_bool = True

        # TODO : 	    "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
        # ADD link instead

        friends = []
        friends.append(author.id)
        friends.append(author2.id)

        response_data = OrderedDict()
        response_data['query'] = 'friends'
        response_data['authors'] = friends
        response_data['friends'] = friends_bool

        return Response(response_data)

# Return current friend_requests

class AuthorFriendRequestsView(APIView):

    """
    List of Friend Requersts for Author.
    ---
    get:
        parameters_strategy:
            form: replace
        parameters:
            - id: uuid
              user: name
              displayName:
              bio:
              posts_created: number
              github_url: string
              friends: list
              following: list
              followers: list
    """

    serializer_class = AuthorSerializer
    model = Author
    queryset = Author.objects.all()

    def get(self, request, pk, *args, **kwargs):

        author = get_object_or_404(models.Author, id= pk)

        author_serializer = AuthorSerializer(author)
        response_data = OrderedDict()
        response_data['query'] = 'friends'
        response_data['author'] = author.id
        response_data['friend_requests'] = author_serializer.data["followers"]

        return Response( response_data ) 

# https://docs.djangoproject.com/en/2.1/ref/class-based-views/base/#redirectview

class AuthorFriendRequestActionsView( RedirectView):

    """
    Reource for Friend Request Actions.
    ---
    get_redirect_url:
        parameters_strategy:
            form: replace
        parameters:
            - id: uuid
              user: name
              displayName:
              bio:
              posts_created: number
              github_url: string
              friends: list
              following: list
              followers: list
    """

    serializer_class = AuthorSerializer
    model = Author
    queryset = Author.objects.all()

    def get_redirect_url(self, *args, **kwargs):    
        
        target_pk = kwargs.get('pk')
        method = kwargs.get('method')
        sender = self.request.user

        target_author = get_object_or_404(models.Author, pk= target_pk)
        sender_author = get_object_or_404(models.Author, user=user)

        # Our sender is accepting the target author requests

        if method == "accept":
           sender_author.respond_to_friend_request(target_author, "accept")

        if method == "decline":
            sender_author.respond_to_friend_request(target_author, "decline")

        if method == "send-request":
            
            sender.send_friend_request(target_author)   # target is sending request to the sender. 

        if method == "unfriend":
            sender_author.remove(target_author)