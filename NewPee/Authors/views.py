from Authors.models import Author
from Authors.serializers import AuthorSerializer
from collections import OrderedDict
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from itertools import chain
from Posts.models import Post, ForeignPost, Photo
from Posts.serializers import PostSerializer, ForeignPostSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from Servers.models import Server
from views import api_views
from views.forms import SearchForm
from django.urls import reverse_lazy
import operator
import uuid
from views.api_views import post_list
class AuthorDetail(APIView):

    """
    Retrieve, update or delete an Author.
    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'

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

            servers = Server.objects.all()

            for x in servers:

                print(x.isServerActive(), x, "\n\n\n\n\n\n\n")

                if x.isServerActive():

                    #x.updateAuthors()
                    x.updatePosts()




            author = self.get_object(pk)
            author_serializer = AuthorSerializer(author, context = {'request': request})
            logged_in_author = Author.objects.get(user = request.user)
            logged_in_author_serializer = AuthorSerializer(logged_in_author, context= {'request': request})
            form = SearchForm()
            search = request.GET.get('search')

            


            if search:

                exclude_author = Author.objects.filter(user = request.user)
                authors = Author.objects.filter(displayName__icontains = search).exclude(pk__in=exclude_author)

                print(authors)

                return Response({'authors': authors, 'form': form, 'search': search}, template_name='search.html')

            try:

                response = post_list(request._request)

                print(response, "\n\n\n\n\n\n\n")

                cursor = response.data["posts"]


                for index in range(len(cursor)-1, -1, -1):
                    if uuid.UUID(cursor[index]["author"]["id"].split("/")[-1]) != author.id:
                        cursor.pop(index)

                response_list = list(cursor)
                response_list.sort(key=lambda x: x['post_date'], reverse=True)
                paginator = Paginator(response_list, 5)
                page = request.GET.get('page')
                pages = paginator.get_page(page)

                followers = author.get_followers()
                following = author.get_following()




                if(logged_in_author not in followers):
                    followingBool = True
                else:
                    followingBool = False


                return Response({'author': author_serializer.data, 'current_author':logged_in_author_serializer.data, \
                'form': form, 'logged_in_author':logged_in_author_serializer.data, \
                'pages': pages, 'followers': followers, 'following': following, 'followingBool' : followingBool })

            except Post.DoesNotExist:

                foreignposts = ForeignPost.objects.all()
                foreignposts_serializer = ForeignPostSerializer(foreignposts, many=True)

                return Response({'author': author_serializer.data, 'form': form, \
                    'foreignposts': foreignposts_serializer.data})

    # Clean Up After
    def post(self, request, pk, *args, **kwargs):


        if request.method == 'POST' and request.FILES['myfile']:

            author = self.get_object(pk)
            author_serializer = AuthorSerializer(author,context={'request': request})
            logged_in_author = Author.objects.get(user = request.user)
            logged_in_author_serializer = AuthorSerializer(logged_in_author,context={'request': request})
            form = SearchForm()
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
    """

    @csrf_exempt
    def get(self, request, format=None):

        if request.method == "GET":

            print("This is the request\n\n", request)

            authors = Author.objects.all()

            print(authors, "?")

            author_serializer = AuthorSerializer(authors, many=True,context={'request': request})
            posts = Post.objects.all()
            post_serializer = PostSerializer(posts, many=True)

            # print("This is a serializer: ", serializer)
            # print("This is the type: ", type(serializer))
            # print("This is the data inside of serializer", serializer.data)

            return Response({
                'authors': author_serializer.data,
                'posts': post_serializer.data,
            })


#a reponse if friends or not
#ask a service GET http://service/author/<authorid>/friends/

# WORKS
class AuthorfriendsView(APIView):

    @csrf_exempt
    def get(self, request, pk, *args, **kwargs):

            author = get_object_or_404(models.Author, id= pk)
            response_data = OrderedDict()
            response_data['query'] = 'friends'
            response_data['authors'] = author.get_friends().values('id')

            return Response(response_data)

# ask a service if anyone in the list is a friend
# POST to http://service/author/<authorid>/friends

    @csrf_exempt
    def post(self, request, pk, *args, **kwargs):

            author = get_object_or_404(models.Author, id= pk)

            # good request with array of authors
            try:

                authors = request.data["authors"]
                friends = []

                for request_author in authors:
                    our_friends = author.get_friends().values('id')

                    # Check they are friend
                    try:

                        if our_friends.get(id=request_author["id"]):

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
# WORKS
class AuthorIsfriendsView(APIView):

    @csrf_exempt
    def get(self, request, pk, pk2, *args, **kwargs):

        author = get_object_or_404(models.Author, id= pk)
        author2 = get_object_or_404(models.Author, id= pk2)
        ser1 = AuthorSerializer(author, context={'request': request})
        ser2 = AuthorSerializer(author2, context={'request': request})
        friends_bool = False

        if author.is_friend(author2.id) and author2.is_friend(author.id):

            friends_bool = True

        # TODO : 	    "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
        # ADD link instead

        friends = []

        friends.append(ser1.data["id"])
        friends.append(ser2.data["id"])

        response_data = OrderedDict()
        response_data['query'] = 'friends'
        response_data['authors'] = friends
        response_data['friends'] = friends_bool

        return Response(response_data)

# Return current friend_requests
# TO be used with headers.

class AuthorFriendRequestsView(APIView):

    def get(self, request, pk, *args, **kwargs):

        author = get_object_or_404(models.Author, id= pk)

        response_data = OrderedDict()
        response_data['query'] = 'friends'
        response_data['author'] = author.id
        response_data['size'] = 0

        friend_requests = author.get_friend_requests()

        declinedrequest = author.get_declined_requests()

        for friend in declinedrequest:

            friend_requests = friend_requests.exclude(id = friend.id)

        #print(friend_requests, "???")

        friend_serializer = AuthorSerializer(friend_requests, context={'request': request}, many=True)

        #print(friend_serializer.data)

        response_data['friend_requests'] = friend_serializer.data
        response_data['size'] = len(friend_serializer.data)

        return Response( response_data )

# api for friendrequest
# upon recieiving the author that send the friend request add them
class AuthorUpdateFriendRequestsView(APIView):

    def get(self, request):

        return Response(status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):


        print(request)
        print(request.data)

        recieving_author = request.data["author"]   # author recieving request
        friend = request.data["friend"]             # friend being added to author.

        print(friend["id"])
        
        friend_uuid = friend["id"].split("/")[-1]
        recieving_author_uuid = recieving_author["id"].split("/")[-1]

        friend_uuid = friend_uuid.strip(" ")
        author = get_object_or_404(Author, id =  recieving_author_uuid)


        print("\n\n", recieving_author, "\n\n")
        print(friend, "\n\n")


        #try:

            # a local author we can just add them.
        friend = get_object_or_404(Author, id = friend_uuid)

        if request.data["query"] == "declinerequest":

            author.add_friend_request(friend)   # add them into our friend requests, used to hide notifications.
            return Response(status=status.HTTP_201_CREATED)


       
        friend.add_friend(author)
            
                


        return Response(status=status.HTTP_200_OK)

        #except:

        #    return Response(status=status.HTTP_400_BAD_REQUEST)

# https://docs.djangoproject.com/en/2.1/ref/class-based-views/base/#redirectview
class AuthorFriendRequestActionsView( RedirectView):

    def get_redirect_url(self, *args, **kwargs):


        url = reverse_lazy('feed')

        target_pk = kwargs.get('pk')
        method = kwargs.get('method')
        sender = self.request.user
        target_author = get_object_or_404(Author, pk= target_pk)
        sender_author = get_object_or_404(Author, user=sender)

        #sender_author = get_object_or_404(Author, request.data["friend"])


        # Our sender is accepting the target author requests
        if method == "accept":

           sender_author.respond_to_friend_request(target_author, "accept")

        if method == "decline":

            print("GOT HERE")
            sender_author.respond_to_friend_request(target_author, "decline")
            if (sender_author.is_friend(target_author.id)):
                sender_author.remove_friend(target_author)
                target_author.remove_friend(sender_author)



        if method == "send-request":

            sender.send_friend_request(target_author,request,)   # target is sending request to the sender.

        if method == "unfriend":

            sender_author.remove_friend(target_author, request)
            target_author.remove_friend(sender_author, request)

        return url

