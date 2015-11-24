from django.shortcuts import render, redirect
from django.core.exceptions import *
from mainkerrini.forms import RegisterForm, LoginForm
from mainkerrini.models import User, UserLogin


def index(request):
    form = LoginForm()
    return render(request, 'index.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = UserLogin.objects.get(email=form.cleaned_data['email_address'])
            request.session['user_loggedin'] = user.user_id
            return redirect('')
        else:
            raise ValidationError
            return redirect('/')
    form = LoginForm()
    return render(request, 'index.html', {'form': form})


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
            user = User.create(first_name=first_name, last_name=last_name)
            UserLogin.create(email=email, username=username,password=password,user_id=user.user_id)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
