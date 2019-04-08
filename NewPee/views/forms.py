from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from Authors.models import Author

class UserCreateForm(UserCreationForm):

    first_name = forms.CharField(label="First Name", max_length=100, required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
        error_messages = {'required': "First Name is required."})

    last_name = forms.CharField(label="Last Name", max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}),
        error_messages = {'required': "Last Name is required."})

    email = forms.EmailField(label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))

    username = forms.CharField(label="username", max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
        error_messages = {'required': "Username is required."})

    password1 = forms.CharField(label="password", max_length=100, required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        error_messages = {'required': "Password is required."})

    password2 = forms.CharField(label="password", max_length=100, required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
        error_messages = {'required': "Passwords do not match."})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def signup(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password1)

        return new_user


class UserLoginForm(forms.Form):

    username = forms.CharField(label="username", max_length=100, required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Username',  'class': 'form-control'}))

    password = forms.CharField(label="password", required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Invalid username or password. Please try again.")

        validate_user = Author.objects.get(user=user)
        if not validate_user.isAuthorized:
            raise forms.ValidationError("User needs to be authorized by a Server Administrator.")

        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
        

class PostTitleForm(forms.Form):

    post_title = forms.CharField(label="username", max_length=100)

class PostInfoForm(forms.Form):

    post_info = forms.CharField(label="username", max_length=100)

class SearchForm(forms.Form):

    search = forms.CharField(label="search", max_length=50,
                    widget=forms.TextInput(attrs={'placeholder': 'Search for authors', 'id': 'ajax', 'list': 'ajax_authors', 'class': 'form-control'}))

class PasswordLoginForm(forms.Form):

    password = forms.CharField(label="username", max_length=100)

class CommentForm(forms.Form):

    comment = forms.CharField(label="Comment", max_length=100,
                    widget=forms.TextInput(attrs={'placeholder': 'What\'s on your mind?', 'id':'comment', 'class': 'form-control'}))