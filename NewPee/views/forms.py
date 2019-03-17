

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Naming and cleanup
class UserNameForm(UserCreationForm):

    first_name = forms.CharField(label="First Name", max_length=100,
                    widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))

    last_name = forms.CharField(label="Last Name", max_length=100,
                    widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}))

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))

    username = forms.CharField(label="username", max_length=100,
                   widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))

    password1 = forms.CharField(label="password", max_length=100,
                   widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

    password2 = forms.CharField(label="password", max_length=100,
                   widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')



class postTitleForm(forms.Form):
    post_title = forms.CharField(label="username", max_length=100)

class postInfoForm(forms.Form):
    post_info = forms.CharField(label="username", max_length=100)

# 
class UserLoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100,
                    widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))

    password = forms.CharField(label="password", max_length=100,
                    widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

class SearchForm(forms.Form):
    search = forms.CharField(label="search", max_length=50,
                    widget=forms.TextInput(attrs={'placeholder': 'Search by author or keywords', 'id': 'ajax', 'list': 'ajax_authors', 'class': 'form-control'}))

class passwordLoginForm(forms.Form):
    password = forms.CharField(label="username", max_length=100)
