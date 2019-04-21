from __future__ import unicode_literals
from django.db import models
from apps.login_reg_app.models import User
from datetime import datetime
import bcrypt
from dateutil.relativedelta import relativedelta
import re

class BookManager(models.Manager):
    def add_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['new_title'] = "Title is required"
        if len(postData['description']) < 5:
            errors['new_desc'] = "Description must be at least 5 characters long"
        return errors

    def update_validator(self, user_id, book_id, postData): 
        errors = {}
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        if book.added_by.id != user.id: 
            errors['mod_auth'] = "You are not authorized to update this book"
        if len(postData['title']) < 1:
            errors['mod_title'] = "Title is required"
        if len(postData['description']) < 5:
            errors['mod_desc'] = "Description must be at least 5 characters long"
        return errors 
    
    def delete_validator(self, user_id, book_id):
        errors = {}
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        if book.added_by.id != user.id: 
            errors['del_auth'] = "You are not authorized to delete this book"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    added_by = models.ForeignKey(User, related_name="added_books")
    liked_by = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

    def __repr__(self):
        return f"Book: {self.title}"