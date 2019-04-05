from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Naming and cleanup
class UserNameForm(UserCreationForm):

    first_name = forms.CharField(help_text='Required*', label="First Name", max_length=100, 
                    widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))

    last_name = forms.CharField(label="Last Name", max_length=100,
                    widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}))

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))

    username = forms.CharField(label="username", max_length=100,
                   widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
                   error_messages = {'required': "Username is required."})

    password1 = forms.CharField(label="password", max_length=100,
                   widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
                   error_messages = {'required': "Password is required."})

    password2 = forms.CharField(label="password", max_length=100,
                   widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
                   error_messages = {'required': "Passwords do not match."})

    class Meta:

        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class PostTitleForm(forms.Form):

    post_title = forms.CharField(label="username", max_length=100)

class PostInfoForm(forms.Form):

    post_info = forms.CharField(label="username", max_length=100)

class UserLoginForm(forms.Form):

    username = forms.CharField(label="username", max_length=100,
                    widget=forms.TextInput(attrs={'placeholder': 'Username',  'class': 'form-control'}))

    password = forms.CharField(label="password", max_length=100,
                    widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

class SearchForm(forms.Form):

    search = forms.CharField(label="search", max_length=50,
                    widget=forms.TextInput(attrs={'placeholder': 'Search for authors', 'id': 'ajax', 'list': 'ajax_authors', 'class': 'form-control'}))

class PasswordLoginForm(forms.Form):

    password = forms.CharField(label="username", max_length=100)

class CommentForm(forms.Form):

    comment = forms.CharField(label="comment", max_length=100,
                    widget=forms.TextInput(attrs={'placeholder': 'What\'s on your mind?', 'id':'comment', 'class': 'form-control'}))