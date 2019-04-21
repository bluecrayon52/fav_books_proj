from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.all_books),

    url(r'^new_book$', views.new_book),
    url(r'^(?P<id>\d+)$', views.book_detail),

    url(r'^(?P<id>\d+)/add_favorite$', views.add_favorite),
    url(r'^(?P<id>\d+)/add_favorite_detail$', views.add_favorite_detail),

    url(r'^(?P<id>\d+)/un_favorite$', views.un_favorite),
    url(r'^(?P<id>\d+)/un_favorite_detail$', views.un_favorite_detail),

    url(r'^(?P<id>\d+)/update$', views.update),
    url(r'^(?P<id>\d+)/delete$', views.delete),
]