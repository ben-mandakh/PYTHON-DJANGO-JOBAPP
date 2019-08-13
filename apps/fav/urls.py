from django.conf.urls import url
from . import views	

urlpatterns = [
        url(r'^$', views.index),
        url(r'^process$', views.process),
        url(r'^success$', views.success),
        url(r'^login$', views.login),
        url(r'^logout$', views.logout),
        url(r'^books$', views.book),
        url(r'^books/show$', views.booksShow),
        url(r'^shows/(?P<id>\d+)$', views.showOne),
        url(r'^shows/(?P<id>\d+)/update$', views.update),
        # url(r'^shows/(?P<id>\d+)/update$', views.updateDesc),
        # url(r'^shows/(?P<id>\d+)/update$', views.editShowFunction),
        url(r'^shows/(?P<id>\d+)/delete$', views.delete),
        # url(r'^shows/(?P<id>\d+)/delete$', views.delete),
        url(r'^shows/(?P<id>\d+)/unfavor$', views.unfavorite),
]