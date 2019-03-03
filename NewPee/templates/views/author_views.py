from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .forms import UserNameForm
from Authors.models import Author
from django.contrib.auth.models import User

# Create your views here.
def log_in(request):
    return render(request, 'login.html', {})

def sign_up(request):



    if request.method == 'POST':

        form = UserNameForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            temp_user = User.objects.create(username=username)

            new_user = Author.objects.create(user=temp_user)



            return HttpResponse(new_user)
            #return HttpResponseRedirect('/thanks/')
    else:
        form = UserNameForm()




    return render(request, 'signup.html', {'form': form})
