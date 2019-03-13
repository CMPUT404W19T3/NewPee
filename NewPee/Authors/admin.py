from django.contrib import admin
from django.contrib.auth.models import User
from .models import Author

# Register models.


# Register custom user
admin.site.register(Author)