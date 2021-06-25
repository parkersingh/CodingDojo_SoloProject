from typing import ContextManager
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from .models import User, Movie, Review, Comment

# Create your views here.


def index(request):
    return render(request, 'index.html')

# create creates new user only with POST status and sends
# new user to dashboard or returns any errors made while registering


def create(request):
    if request.method == 'GET':
        return redirect('/')

    errors = User.objects.validator(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/dashboard')

# logs existing users in to dashboard only with POST status


def login(request):
    if request.method == 'GET':
        return redirect('/')

    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')

    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id

    return redirect('/dashboard')

# logout logs user out of app and returns to register/login page

def logout(request):
    request.session.flush()
    return redirect('/')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "movies": Movie.objects.all(),
        "reviews": Review.objects.all(),
    }
    return render(request, "dashboard.html", context)


def new_movie(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'new_movie.html', context)


def add_movie(request):
    if request.method == 'GET':
        return redirect('/movie/new')

    errors = Movie.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
            return redirect('/movie/new')

    movie = Movie.objects.add(request.POST, request.FILES['poster'])
    return redirect('/dashboard')

def show_movie(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'movie': Movie.objects.get(id=movie_id),
        'reviews': Review.objects.filter(movie = Movie.objects.get(id= movie_id)),
        'user_review': Review.objects.filter(user=User.objects.get(id=request.session['user_id']), 
        movie=Movie.objects.get(id=movie_id)),
    }
    return render(request, 'show_movie.html', context)

def add_review(request):
    if request.method == "GET":
        return redirect('/dashboard')
    
    new_reivew = Review.objects.add(request.POST)

    return redirect(f'/movie/{request.POST["movie_id"]}')

def add_comment(request):
    if request.method == "GET":
        return redirect('/dashboard')

    new_comment = Comment.objects.add(request.POST)

    return redirect(f'/movie/{request.POST["movie_id"]}')

def all_users(request):
    context = {
        'user': User.objects.get(id= request.session['user_id']),
        "all_users": User.objects.exclude(id= request.session['user_id']),
    }
    return render(request, 'all_users.html', context)

def show_profile(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'user': User.objects.get(id= user_id),
        'user_reviews': Review.objects.filter(user= User.objects.get(id= user_id)),
        'session_user': User.objects.get(id= request.session['user_id']),
    }

    return render(request, 'show_profile.html', context)

def edit_user(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'user': User.objects.get(id= request.session['user_id']),
    }

    return render(request, 'edit_profile.html', context)

def update_user(request):
    if request.method == 'GET':
        return redirect('/dashboard')
    
    user_update = User.objects.update(request.POST)

    return redirect(f'/user/{ request.POST["user_id"]}')

def delete_user(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    user_delete = User.objects.get(id= request.session['user_id'])
    user_delete.delete()
    request.session.flush()
    return redirect('/')
    
