from django.contrib import admin
from django.contrib.auth.models import User
from .Authors import Author
from .Posts import Post, Comment


# Register models.

# Unregister default user
admin.site.register(User)

# Register custom user
admin.site.register(User, Author)
admin.site.register(Post)
admin.site.register(Comment)
