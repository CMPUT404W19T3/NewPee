# Import all the models

from .author import Author
from .posts import Post, Comment

__all__ = [
    'Author', 
    'Post', 
    'Comment',
]