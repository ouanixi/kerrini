import datetime

from django.shortcuts import render, redirect, HttpResponse
from mainkerrini.models import *
from cassandra.cqlengine.query import LWTException, CQLEngineException
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
        redirect('/login/')
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


# TODO handle tags.  
def add_video(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            path_and_codec = handle_uploaded_file(file)
            vid = Video.create(data=path_and_codec[1], language=form.cleaned_data['language'],
                               title=form.cleaned_data['title'], user_id=user_id,
                               description=form.cleaned_data['description'], category=form.cleaned_data['category'],
                               date_created=datetime.datetime.now(), video_codec=path_and_codec[0])
            VideoUser.create(user_id=user_id, video_id=vid.video_id, category=form.cleaned_data['category'])
            return redirect('/play/' + str(vid.video_id))
    else:
        form = VideoForm()
    return render(request, 'addvideo.html', {'form': form})


def play(request, uuid):
    try:
        video = Video.get(video_id=uuid)
    except Video.DoesNotExist:
        return redirect('/profile/') # needs to be redirected to some error page.
    return render(request, 'play.html', {'video': video})


def my_videos(request):
    try:
        user = request.session['user_id']
        videos = VideoUser.objects.filter(user_id=user)
        my_vids = []
        for vid in videos:
            my_vids = my_vids + [Video.objects.get(video_id=vid.video_id)]
        print(my_vids)
    except KeyError:
        return redirect('/login/')

    return render(request, 'my_videos.html', {'my_videos': my_vids})


def browse(request):
    videos = Video.objects.all().limit(100)
    categories = Category.objects.all()
    return render(request, 'browse.html', {'all_videos': videos, 'categories': categories})


def add_video_to_new_playlist(request, video_id):
    user = request.session['user_id']
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            new_playlist = UserPlaylist.create(user_id=user, playlist_name=form.cleaned_data['playlist_name'],
                                               category=form.cleaned_data['category'],
                                               description=form.cleaned_data['description'])
            Playlist.create(playlist_id=new_playlist.playlist_id, user_id=user, video_id=video_id)
            return redirect('/view_playlist/' + str(new_playlist.playlist_id))
    else:
        form = PlaylistForm()
    return render(request, 'add_video_to_new_playlist.html', {'form': form})


def add_to_existing_playlist(request, video_id):
    video_id = video_id
    if request.method == 'POST':
        print(request.POST['somename'])
        return redirect('/view_playlist/')
    else:
        try:
            playlists = UserPlaylist.objects.filter(user_id=request.session['user_id'])
        except KeyError:
            return redirect('/login/')

    return render(request, 'add_video_to_existing_playlist.html', {'playlists': playlists, 'video': video_id})


# def create_new_playlist(request):
#     user = request.session['user_id']
#     if request.method == 'POST':
#         form = PlaylistForm(request.POST)
#         if form.is_valid():
#             new_playlist = UserPlaylist.create(user_id=user, playlist_name=form.cleaned_data['playlist_name'],
#                                                category=form.cleaned_data['category'],
#                                                description=form.cleaned_data['description'])
#             Playlist.create(playlist_id=new_playlist.playlist_id, user_id=user)
#             return redirect('/view_playlist/' + str(new_playlist.playlist_id))
#     else:
#         form = PlaylistForm()
#     return render(request, 'add_video_to_new_playlist.html', {'form': form})


def view_playlist_details(request, playlist_id):
    playlist = Playlist.objects.filter(playlist_id=playlist_id)
    user_playlist = UserPlaylist.filter(user_id=request.session['user_id'])
    videos = []
    for item in playlist:
        videos += Video.get(video_id=item.video_id)

    return render(request, 'view_playlist.html', {'vid_list': videos, 'playlist': user_playlist})


def my_playlists(request):
    user = request.session['user_id']
    categories = Category.objects.all()
    playlists = UserPlaylist.filter(user_id=user)
    return render(request, 'my_playlists.html', {'playlists': playlists, 'categories': categories})