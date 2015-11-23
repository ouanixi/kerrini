from django.shortcuts import render, redirect
from mainkerrini.forms import RegisterForm
from mainkerrini.models import User, UserLogin
import bcrypt


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, '')


def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email_address'].lower()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User(first_name=first_name, last_name=last_name)
            user.save()
            userlogin = UserLogin(email=email, username=username,password=password,user_id=user.user_id)
            userlogin.save()
            # ...
            # redirect to a new URL:

            return redirect('/kerri/index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
