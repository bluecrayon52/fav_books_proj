from django.shortcuts import render, redirect
from django.contrib import messages
from apps.login_reg_app.models import User
from .models import Book

def all_books(request):
    if 'user_id' not in request.session:
        return redirect("/")
        
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "user": user,
        "books": Book.objects.all(),
        "favorite_ids": user.liked_books.values_list("id", flat=True)
    }
    return render(request, "fav_books_app/all_books.html", context)

def new_book(request):
    if 'user_id' not in request.session:
        return redirect("/")

    user = User.objects.get(id=request.session['user_id'])
    errors = Book.objects.add_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
    else: 
        book = Book.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            added_by= user
        )
        book.liked_by.add(user)
    return redirect("/books")

def book_detail(request, id):
    if 'user_id' not in request.session:
        return redirect("/")

    user = User.objects.get(id=request.session['user_id'])
    context ={
        "user": user,
        "book": Book.objects.get(id=id),
        "favorite_ids": user.liked_books.values_list("id", flat=True)
    }
    return render(request, "fav_books_app/book_detail.html", context)

# helper function 
def add_favorite_helper(request, id):
    if 'user_id' not in request.session:
        return redirect("/")

    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    book.liked_by.add(user)
    return True

def add_favorite(request, id):
    added = add_favorite_helper(request, id)
    return redirect("/books")

def add_favorite_detail(request, id):
    added = add_favorite_helper(request, id)
    return redirect(f"/books/{id}")

# helper function 
def un_favorite_helper(request, id):
    if 'user_id' not in request.session:
        return redirect("/")

    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    book.liked_by.remove(user)
    return True

def un_favorite(request, id):
    un_faved = un_favorite_helper(request, id)
    return redirect("/books")

def un_favorite_detail(request, id):
    un_faved = un_favorite_helper(request, id)
    return redirect(f"/books/{id}")

def update(request, id):
    if 'user_id' not in request.session:
        return redirect("/")

    errors = Book.objects.update_validator(request.session['user_id'], id, request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
    else: 
        book = Book.objects.get(id=id)
        book.title = request.POST['title']
        book.description = request.POST['description']
        book.save()
    return redirect(f"/books/{id}")

def delete(request, id):
    if 'user_id' not in request.session:
        return redirect("/")

    errors = Book.objects.delete_validator(request.session['user_id'], id)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
    else: 
        Book.objects.get(id=id).delete()
    return redirect("/books")
