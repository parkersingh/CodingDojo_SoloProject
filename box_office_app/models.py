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
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"

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
            first_name = postData['first_name'],
            last_name = postData['last_name'],
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

class User(models.Model):
    first_name = models.CharField(max_length= 255)
    last_name = models.CharField(max_length= 255)
    email = models.EmailField(unique= True)
    password = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

