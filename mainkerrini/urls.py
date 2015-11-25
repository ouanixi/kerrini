from django.conf.urls import url
from mainkerrini import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/login$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit$', views.edit, name='edit'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_result/$', views.search_result, name='search_result'),
]

