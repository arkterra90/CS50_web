from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import *


def index(request):

    allPost = Post.objects.all().order_by('-timeStamp')
    paginator = Paginator(allPost, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    has_previous_page = page_obj.has_previous
    
    print(page_obj.count)
    return render(request, "network/index.html", {
        "allPost": allPost,
        "page_obj": page_obj,
        "has_previous_page": has_previous_page
    })

def post(request):
    if request.method == "POST":
        text = request.POST.get("newPostBox")
        if text:
            try:
                Post.create_post(user=request.user, text=text)
            except IntegrityError:
                return render(request, "network/index.html", {
                    "message": "Could Not Create New Post"
                })

    return render(request, "network/index.html")



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def user(request):

    logged_in_user = request.user

    # Gets all post made by active user
    userPost = Post.objects.filter(user = request.user).order_by('-timeStamp')

    #Gets all needed info for profile page
    user_info = User.objects.filter(username = logged_in_user.username).first()

    print(userPost)
    return render(request, "network/user.html")