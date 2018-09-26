from django.shortcuts import render
from .models import *
import bcrypt
def index(request):
    return render(request,'index.html')
def register(request):
    valid,response=User.objects.validate_registration(request.POST)
    if valid:
        request.session['message']="successfully registered an account!"
        User.objects.create(name=request.POST['name'],alias=request.POST['alias'],email=request.POST['email'],password= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
    else:
        request.session['message']="Failed to registered !"
        request.session['errors']=response
    return render(request,'result.html')
def login(request):
    valid,response=User.objects.validate_login(request.POST)
    if valid:
        request.session['message']="successfully logined !"
        request.session['login_id']=User.objects.get(email=request.POST['email']).id
        context={
            "user":User.objects.get(email=request.POST['email']).name,
            "reviews": Review.objects.all().order_by('id')
        }
        return render(request,'home.html',context)
    else:
        request.session['message']="Failed to login !"
        request.session['errors']=response
        return render(request,'result.html')
def logout(request):
    del request.session['login_id']
    return render(request,'index.html')
def add_review(request):
    return render(request,'add_review.html')
def process_review(request):
    try:
        Book.objects.get(title=request.POST['title'])
    except:
        Book.objects.create(title=request.POST['title'],author=request.POST['author'],user=User.objects.get(id=request.session['login_id']))
    Review.objects.create(comment=request.POST['review'],rating=request.POST['rating'],user=User.objects.get(id=request.session['login_id']),books=Book.objects.get(title=request.POST['title']))
    context={
        "book":Book.objects.get(title=request.POST['title']),
        "reviews":Review.objects.filter(books=Book.objects.get(title=request.POST['title']))

    }
    return render(request,'specific_book.html',context)
def user(request,user_id):
    user1=User.objects.get(id=user_id)
    context={
        "user1":user1,
        "books":Book.objects.filter(user=user1),
        "reviews": Review.objects.filter(user=user1)
    }
    return render(request,'specific_user.html',context)
def back(request):
    context={
        "user":User.objects.get(id=request.session['login_id']).name,
        "reviews": Review.objects.all().order_by('id')
    }
    return render(request,'home.html',context)
# Create your views here.
