from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create', views.create),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('movie/new', views.new_movie),
    path('movie/add', views.add_movie),
    path('movie/<int:movie_id>', views.show_movie),
    path('review/add', views.add_review),
    path('comment/add', views.add_comment),
]