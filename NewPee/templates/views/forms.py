

from django import forms


class UserNameForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)

class postTitleForm(forms.Form):
    post_title = forms.CharField(label="username", max_length=100)

class postInfoForm(forms.Form):
    post_info = forms.CharField(label="username", max_length=100)

class userLoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)

class passwordLoginForm(forms.Form):
    password = forms.CharField(label="username", max_length=100)
