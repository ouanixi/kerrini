import os

from django.shortcuts import render, redirect, HttpResponse
from kerrini.settings import STATIC_ROOT
from mainkerrini.models import *
from cassandra.cqlengine.query import LWTException
from mainkerrini.forms import *
from django.core.files.base import ContentFile

def index(request):
    form = LoginForm()
    return render(request, 'index.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_login = UserLogin.objects.get(email=form.cleaned_data['email_address'])
            request.session['user_id'] = user_login.user_id
            request.session['username'] = user_login.username
            return redirect('/profile')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email_address'].lower()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                # insert into userlogin if username is not taken
                UserLogin.if_not_exists().create(username=username, email=email, password=password)
                user = User.create(first_name=first_name, last_name=last_name)
                user_login = UserLogin.objects.get(username=username)
                user_login.user_id = user.user_id
                user_login.save()
                Picture.create(user_id=user.user_id)
                request.session['user_id'] = user_login.user_id
                request.session['username'] = user_login.username
                return redirect('/profile')
            except LWTException:
                return HttpResponse("LWT failed")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def profile(request):
    try:
        user = User.objects.get(user_id=request.session['user_id'])
        user_login = UserLogin.objects.get(username=request.session['username'])
        picture = Picture.objects.get(user_id=user.user_id)
    except(KeyError, User.DoesNotExist):
        user = None
        user_login = None
        redirect('/login')
    return render(request, 'profile.html', {'user_login': user_login, 'user': user, 'picture': picture})

def edit(request):
    user = User.objects.get(user_id=request.session['user_id'])
    if request.method == 'POST':
        form = AccountForm(request.POST)
        print("post edit")
        if form.is_valid():
            print("post edited")
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            bio = form.cleaned_data['bio']
            user.first_name = first_name
            user.last_name = last_name
            user.bio = bio
            user.save()
            return redirect('/edit')
    else:
        form = AccountForm(initial={'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'bio': user.bio})
    return render(request, 'edit.html', {'form': form})

def logout(request):
    try:
        del request.session['user_id']
        del request.session['username']
    except KeyError:
        redirect("/login/")
    return redirect("/")

def picture(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            folder = request.path.replace("/", "_")
            uploaded_filename = request.FILES['image'].name
            # create the folder if it doesn't exist.
            try:
                print("trying")
                os.makedirs(os.path.join(STATIC_ROOT, folder))
            except:
                print("failse")
                pass

            # save the uploaded file inside that folder.
            full_filename = os.path.join(STATIC_ROOT, folder, uploaded_filename)
            fout = open(full_filename, 'wb+')
            file_content = ContentFile(request.FILES['image'].read())

            try:
                for chunk in file_content.chunks():
                    fout.write(chunk)
                fout.close()
                picture = Picture.objects.get(user_id=request.session['user_id'])
                picture.data = full_filename
                picture.save()
                return redirect('/profile')
            except:
                return redirect('/picture')
    else:
        form = ImageForm()
    return render(request, 'uploadimage.html', {'form': form})

def search(request):
    return render(request, 'search.html')

def search_result(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

