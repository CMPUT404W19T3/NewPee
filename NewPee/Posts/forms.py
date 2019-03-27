from django import forms

from .models import Posts

class PostForm(forms.ModelForm):

    # Define Validation 

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        # Define more validation
        return title

    def clean_description(self, *args, **kwargs):
        description = self.cleaned_data.get("description")
        # Define more validation
        return description

    def clean_content(self, *args, **kwargs):
        content = self.cleaned_data.get("body")
        # Define more validation
        return content

# class ImageUploadForm (forms.Form):
#     title = forms.CharField(max_length=50)
#     file = forms.ImageField()