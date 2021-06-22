from django.db import models
from datetime import datetime, timedelta

import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# UserManager overrides User.objects
class UserManager(models.Manager):
    # validator validates all registration data for new user
    def validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Name should be at least 2 characters"
        
        if len(User.objects.filter(username = postData['username'])) == 1:
            errors['username'] = "Username is already taken. Please choose a different username"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        
        if postData['password'] != postData['confirm_pw']:
            errors['password'] = "Passwords do not match"

        return errors
    
    # register takes registration data and creates a new User from that data
    def register(self, postData):
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()

        return User.objects.create(
            name = postData['name'],
            username = postData['username'],
            email = postData['email'],
            password = pw
        )
    
    # authenticate logs in existing users
    def authenticate(self, email, password):
        users = User.objects.filter(email= email)
        if users:
            user = users[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
            else:
                return False
        return False

class MovieManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Title of movie is required"
        
        if len(postData['genre']) < 1:
            errors['genre'] = "Genre of movie is required"
        
        if len(postData['director']) < 1: 
            errors['director'] = "Director of movie is required"

        if len(postData['description']) < 1:
            errors['description'] = "Description of movie is required"
        
        return errors
    
    def add(self, postData):
        return Movie.objects.create(
            title = postData['title'],
            genre = postData['genre'],
            director = postData['director'],
            description = postData['description'],
            avg_rating = 0,
            poster = postData['poster'],
            added_by = User.objects.get(id= postData['user_id'])
        )


class User(models.Model):
    name = models.CharField(max_length= 255)
    username = models.CharField(max_length= 255)
    email = models.EmailField(unique= True)
    password = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

class Movie(models.Model):
    title = models.CharField(max_length= 255)
    genre = models.CharField(max_length= 255)
    director = models.CharField(max_length= 255)
    description = models.TextField()
    avg_rating = models.IntegerField()
    poster = models.ImageField(upload_to='images/')
    added_by = models.ForeignKey(User, related_name= "added_movies", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = MovieManager()

class Rating(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User, related_name='user_ratings', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

class Review(models.Model):
    review_content = models.TextField()
    user = models.ForeignKey(User, related_name='user_reviews', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

class Comment(models.Model):
    comment_content = models.TextField()
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_comments',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)



