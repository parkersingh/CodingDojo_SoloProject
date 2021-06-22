from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from .models import User, Movie, Rating, Review, Comment

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

    user = User.objects.get(email= request.POST['email'])
    request.session['user_id'] = user.id

    return redirect('/dashboard')

# logout logs user out of app and returns to register/login page
def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id= request.session['user_id'])

    context = {
        "user": user,
    }
    return render(request, "dashboard.html", context)

def new_movie(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id= request.session['user_id'])
    }
    return render(request, 'new_movie.html', context)

def add_movie(request):
    if request.method == 'GET':
        return redirect('/movies/new')
    
    errors = Movie.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
            return redirect('/movies/new')

    movie = Movie.objects.add(request.POST)
    return redirect('/dashboard')

def show_movie(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id= request.session['user_id']),
        'movie': Movie.objects.get(id= movie_id),
    }
    return render(request, 'show_movie.html', context)