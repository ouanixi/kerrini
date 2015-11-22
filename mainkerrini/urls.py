from django.conf.urls import url
from mainkerrini import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^$/register/', views.register, name='register'),
]

