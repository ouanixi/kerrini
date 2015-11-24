from django.shortcuts import render, redirect, HttpResponse
from mainkerrini.forms import RegisterForm
from mainkerrini.models import User, UserLogin, Vote
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.query import LWTException
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
            # check if user already has account (i.e. email already exists)
            if UserLogin.objects.filter(email=email):
                return HttpResponse("email in use")
            # insert first/last name into user table
            user = User.create(first_name=first_name, last_name=last_name)
            try:
                # insert into userlogin if username is not taken
                UserLogin.if_not_exists().create(username=username, email=email,
                                                 password=password, user_id=user.user_id)
                return HttpResponse("done")
            except LWTException:
                # remove user entry as LWT failed
                user.objects.filter(user_id=user.user_id).delete()
                return HttpResponse("LWT failed")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def search(request):
    return render(request, 'search.html')

def search_result(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)