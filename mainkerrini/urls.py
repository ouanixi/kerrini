from django.conf.urls import url

from kerrini import settings
from mainkerrini import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'/register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'/login/$', views.login, name='login'),
    url(r'/logout/$', views.logout, name='logout'),
    url(r'^upload_picture/$', views.upload_picture, name='picture'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_result/$', views.search_result, name='search_result'),
    url(r'^play/$', views.play, name='play_video'),
    url(r'^add_video/$', views.add_video, name='play_video'),

]

