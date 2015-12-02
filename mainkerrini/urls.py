from django.conf.urls import url

from kerrini import settings
from mainkerrini import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^video_vote/$', views.video_vote, name='video_vote'),
    url(r'^add_video_link/$', views.add_video_link, name='add_video_link'),
    url(r'/logout/$', views.logout, name='logout'),
    url(r'^browse/$', views.browse, name='browse'),
    url(r'^upload_picture/$', views.upload_picture, name='picture'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit'),
    url(r'^play/(?P<uuid>[^/]+)/$', views.play, name='play_video'),
    url(r'^add_video/$', views.add_video, name='add_video'),
    url(r'^my_videos/$', views.my_videos, name='my_videos'),
    url(r'^my_playlists/$', views.my_playlists, name='my_playlists'),
    url(r'^add_to_playlist/(?P<video_id>[^/]+)/$', views.add_to_existing_playlist, name='add_to_existing_playlist'),
    url(r'^create_playlist/(?P<video_id>[^/]+)/$', views.add_video_to_new_playlist, name='add_to_new_playlist'),
    url(r'^view_playlist/(?P<playlist_id>[^/]+)/$', views.view_playlist_details, name='view_playlist'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^get_links/$', views.get_links, name='get_links'),

]

