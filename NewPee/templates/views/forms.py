

from django import forms


class UserNameForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
