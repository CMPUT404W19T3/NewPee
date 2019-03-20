

from Authors.models import Author
from django.contrib.auth.models import User

class GeneralBuilding:


    def create_author(self, username="temp_user", displayName = "temp_name", email="temp@gmail.com", password="TestPass1", ):

        data = {'username':username, 'email':email, 'password': password}

        user = User.objects.create(**data)
        user.save()
        author = Author.objects.create(user)
        author.displayName = displayName

        return author


    def create_authors(usernames):

        for username in usernames:
            email= username + '@gmail.com'
            displayName =  username
            GeneralBuilding.create_author(username=username, email= email, displayName = displayName)



Factory = GeneralBuilding()

