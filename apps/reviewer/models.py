from __future__ import unicode_literals
import bcrypt
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validate_registration(self,form):
        errors=[]
        if len(form['name'])<2:
            errors.append('name must be longer than 2 characters!')
        if len(form['alias'])<2:
            errors.append('alias must be longer than 2 characters!')
        if len(form['password'])<8:
            errors.append('password must be longer than 2 characters!')
        if not EMAIL_REGEX.match(form['email']):
            errors.append('the email you entered is not valid!')
        if form['password']!=form['confirm']:
            errors.append('the confirmed password must match with the the password!')
        try:
            user=self.get(email=form['email'])
            errors.append('the email you used is already registered')
            return (False,errors)
        except:
            if len(errors)>0:
                return (False,errors)
            else:
                return (True,errors)
    def validate_login(self,form):
        errors=[]
        try:
            user=self.get(email=form['email'])
            if bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                return (True,errors)
        except:
            errors.append('the user does not exist')
            return (False,errors)

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=25)
    objects = UserManager()
class Book(models.Model):
    
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="books")
class Review(models.Model):
    comment = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="reviews")
    books = models.ForeignKey(Book, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add = True)
# Create your models here.
