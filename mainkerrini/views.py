import datetime

from django.shortcuts import render, redirect, HttpResponse
from mainkerrini.models import *
from cassandra.cqlengine.query import LWTException
from mainkerrini.forms import *
from django.core.files.base import ContentFile
from mainkerrini.custom_functions import *


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
        try:
            picture = Picture.objects.get(user_id=user.user_id)
        except Picture.DoesNotExist:
            picture = Picture(data='images/avatar.jpg', user_id=user.user_id)
    except(KeyError, User.DoesNotExist):
        redirect('/login')
    return render(request, 'profile.html', {'user_login': user_login, 'user': user, 'picture': picture})


def edit_profile(request):
    user = User.objects.get(user_id=request.session['user_id'])
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            bio = form.cleaned_data['bio']
            user.first_name = first_name
            user.last_name = last_name
            user.bio = bio
            user.save()
            return redirect('/profile')
    else:
        form = AccountForm(initial={'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'bio': user.bio})
        try:
            picture = Picture.objects.get(user_id=user.user_id)
        except Picture.DoesNotExist:
            picture = Picture(data='images/avatar.jpg', user_id=user.user_id)
    return render(request, 'edit_profile.html', {'form': form, 'picture': picture})


def logout(request):
    try:
        del request.session['user_id']
        del request.session['username']
    except KeyError:
        redirect("/login/")
    return redirect("/")


def upload_picture(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            folder = 'profile_pics'
            uploaded_filename = request.session['username'] + '.' + request.FILES['image'].name
            db_path = handle_upload_picture(folder, uploaded_filename, ContentFile(request.FILES['image'].read()))
            try:
                picture = Picture.objects.get(user_id=request.session['user_id'])
                picture.user_id = request.session['user_id']
                picture.data = db_path
                picture.save()
                print("in try")
            except Picture.DoesNotExist:
                Picture.create(user_id=request.session['user_id'], data=db_path)
                print("does not exist")

        return redirect('/profile/')
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})


def search(request):
    return render(request, 'search.html')


def search_result(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)


def add_video(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            path_and_codec = handle_uploaded_file(file)
            Video.create(data=path_and_codec[1], language=form.cleaned_data['language'],
                         title=form.cleaned_data['title'], user_id=user_id,
                         description=form.cleaned_data['description'],
                         date_created=datetime.datetime.now(), video_codec=path_and_codec[0])
            return redirect('/profile/')
    else:
        form = VideoForm()
    return render(request, 'addvideo.html', {'form': form})


def play(request, uuid):
    try:
        video = Video.get(video_id=uuid)
    except Video.DoesNotExist:
        return redirect('/profile/') # needs to be redirected to some error page.
    return render(request, 'play2.html', {'video': video})

# def play(request):
#     current_url = request.get_full_path()
#     filename=current_url.rsplit('/',1)[1]
#     if filename:
#         videos= Video.objects.filter(video_id=filename).allow_filtering()
#         video=videos.get()
#         print(video)
#         return render(request, 'play.html', {'video': video})
#     return render(request, 'play.html')