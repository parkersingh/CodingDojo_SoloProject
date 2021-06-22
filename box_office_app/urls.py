from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create', views.create),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('movies/new', views.new_movie),
    path('movies/add', views.add_movie),
    path('movie/<int:id>', views.show_movie),
]