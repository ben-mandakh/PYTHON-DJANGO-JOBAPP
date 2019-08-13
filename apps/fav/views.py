################### IMPORT SECTION ########################
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import User
from .models import Book
import bcrypt

#################### INDEX PAGE ###########################
def index(request):                
    return render(request, "fav/index.html")

#################### REGISTRATION #########################

def process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        newUser=User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password = hashed_password)
        newUser.save()
        request.session['id']=newUser.id
        messages.success(request, "User successfully registered")
        return redirect("/success")

#################### SHOW PAGE ############################

def success(request):                
    context = {
        "user": User.objects.get(id = request.session['id']),
        "books": Book.objects.all()
        }
    return render(request, "fav/show.html", context)

#################### LOGIN ################################

def login(request):
    if (User.objects.filter(email=request.POST['email']).exists()):
        user = User.objects.filter(email=request.POST['email'])[0]
        if (bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())):
            request.session['id'] = user.id
            messages.success(request, "User successfully logged in")
            return redirect('/success')
    messages.success(request, "Password didn't match")
    return redirect('/')

################### ADD BOOK FUNCTION #####################

def book(request):
    if request.method=='POST':
        print("-"*80)
        errors = Book.objects.validator(request.POST)
        if len(errors) > 0:
            for tag, error in errors.items():
                print(tag, error)
                messages.error(request, error, extra_tags=tag)
        else:
            user = User.objects.get(id = request.session['id'])
            favBook=Book.objects.create(title=request.POST['title'], description=request.POST['desc'], uploaded_by = user)
            favBook.save()
            user.liked_books.add(favBook)
    return redirect("/success")

#################### BOOK SHOW FUNCTION ########################

def booksShow(request):                
    context = {"books": Book.objects.all()}
    return redirect("/success")

#################### BOOK SHOW ONE FUNCTION #####################

def showOne(request,id):                
    context = {
        "book": Book.objects.get(id=id),
        "books": Book.objects.all(),
        "user": User.objects.get(id = request.session['id'])
        }
    return render(request, "fav/showOne.html", context)

#################### BOOK SHOW ONE EDIT PAGE #####################

def showOneEdit(request,id):                
    context = {
        "book": Book.objects.get(id=id),
        "books": Book.objects.all(),
        "user": User.objects.get(id = request.session['id'])
        }
    return render(request, "fav/showOneEdit.html", context)

################### UPDATE FUNCTION #############################

def update(request,id):
    u = Book.objects.get(id = id)
    u.title = request.POST['title']
    u.description = request.POST['desc']
    u.save()
    return redirect ('/success')

#################### DELETE FUNCTION ############################
def delete(request,id):
    d = User.objects.get(id = id)
    d.delete()
    # d.save()
    return redirect ('/success')

#################### UNFAVORITE FUNCTION ########################
def unfavorite(request,id):
    un = Book.objects.get(id = id)
    un.delete()
    # d.save()
    return redirect ('/success')

#################### LOGOUT FUNCTION ############################

def logout(request):
    del request.session['id']
    return redirect('/')































# def show_one(request,id):
#     context = {"show": Show.objects.get(id = id)}
#     return render(request, "show/showOne.html", context)

# def editShow(request, id):                
#     context = {"shows": Show.objects.get(id=id)}
#     return render(request, "show/editShow.html", context)    

# def editShowFunction(request,id):
#     errors = Show.objects.basic_validator(request.POST)
#     if len(errors) > 0:
#         for key, value in errors.items():
#             messages.error(request, value)
#         return redirect(f'/shows/{id}/edit')
#     else:
#         u = Show.objects.get(id = id)
#         u.title=request.POST['title']
#         u.network=request.POST['network']
#         u.release_date=request.POST['release_date']
#         u.desc = request.POST['desc']
#         u.save()
#         messages.success(request, "Blog successfully updated")
#         return redirect ("/shows")

# def delete(request,id):
#     d = Show.objects.get(id = id)
#     d.delete()
#     return redirect ("/shows")


