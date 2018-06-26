from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.createUser),
    url(r'login$', views.login),
    url(r'home$', views.home),
    url(r'post$', views.post),
    url(r'user/(?P<uploader_id>\d+)$', views.user),
    url(r'edit/(?P<user_id>\d+)$', views.edit),
    url(r'update/(?P<user_id>\d+)$', views.update),
    url(r'logout$', views.logout),
    url(r'like', views.like),
    url(r'delete/(?P<quote_id>\d+)', views.delete),
]