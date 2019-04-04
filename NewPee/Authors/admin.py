from django.contrib import admin
from django.contrib.auth.models import User
from .models import Author, ForeignAuthor

# Register models.

# Register custom user
admin.site.register(Author)
admin.site.register(ForeignAuthor)