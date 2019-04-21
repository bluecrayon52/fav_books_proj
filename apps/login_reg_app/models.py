from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt
from dateutil.relativedelta import relativedelta
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        NAME_REGEX = re.compile(r'^[A-Za-z]{2,45}$')
        PASS_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)(.{8,15})$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # first name 
        if len(postData['first_name']) < 1:
            errors['first_name'] = "first name required"

        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "first name must be at least 2 characters long and contain only letters"
        # last name 
        if len(postData['last_name']) < 1:
            errors['last_name'] = "last name required"

        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "last name must be at least 2 characters long and contain only letters"
        # birthday 
        if len(postData['birthday']) < 1:
            errors['birthday'] = "birthday field required"

        elif datetime.strptime(postData['birthday'], '%Y-%m-%d') > datetime.now():
            errors['birthday'] = "birthday must be in the past"
        
        elif relativedelta(datetime.now(), datetime.strptime(postData['birthday'], '%Y-%m-%d')).years  < 13:
            errors['birthday'] = "user must be at least 13 years of age"
        # email 
        if len(postData['email']) < 1: 
            errors['email'] = "email required"

        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email address"

        else: 
            all_emails = User.objects.all().values_list('email', flat=True)
            if postData['email'] in all_emails:
                errors['reg_main'] = "a user with that email is already registered"
        # password
        if len(postData['password']) < 1:
            errors['password'] = "password required"

        elif not PASS_REGEX.match(postData['password']):
            errors['password'] = "password must be at least 8 characters long and contain at least one upper case letter and one number"

        else: 
            # confirm password
            if len(postData['confirm_password']) < 1:
                errors['confirm_password'] = "please confirm password"
            
            elif postData['confirm_password'] != postData['password']:
                errors['confirm_password'] = "passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        PASS_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)(.{8,15})$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
         # email 
        is_valid = True
        if len(postData['email']) < 1: 
            errors['login_em'] = "email required"
            is_valid = False
        elif not EMAIL_REGEX.match(postData['email']):
            errors['login_em'] = "invalid email address"
            is_valid = False
        # password
        if len(postData['password']) < 1:
            errors['login_pass'] = "password required"
            is_valid = False
        elif not PASS_REGEX.match(postData['password']):
            errors['login_pass'] = "password must be at least 8 characters long and contain at least one upper case letter and one number"
            is_valid = False
        # creds 
        if is_valid:
            try:
                user = User.objects.get(email=postData['email'])
            except: 
                errors['login_main'] = "you could not be logged in"
            else: 
                if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                    errors['login_main'] = "you could not be logged in"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    birthday = models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"User: {self.first_name} {self.last_name}"