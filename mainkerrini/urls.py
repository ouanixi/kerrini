from django.conf.urls import url

from kerrini import settings
from mainkerrini import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'/logout/$', views.logout, name='logout'),
    url(r'^browse/$', views.browse, name='browse'),
    url(r'^upload_picture/$', views.upload_picture, name='picture'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit'),
    url(r'^play/(?P<uuid>[^/]+)/$', views.play, name='play_video'),
    url(r'^add_video/$', views.add_video, name='add_video'),
    url(r'^my_videos/$', views.my_videos, name='my_videos'),
    url(r'^my_playlists/$', views.my_playlists, name='my_playlists'),
    url(r'^add_to_playlist/(?P<video_id>[^/]+)/$', views.add_to_playlist, name='add_to_playlist'),
    url(r'^create_playlist/(?P<video_id>[^/]+)/$', views.add_video_to_new_playlist, name='add_to_new_playlist'),
    url(r'^create_playlist/$', views.create_new_playlist, name='create_playlist'),
    url(r'^view_playlist/(?P<playlist_id>[^/]+)/$', views.view_playlist, name='view_playlist'),

]

