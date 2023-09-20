import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



from .models import *

from django.http import JsonResponse


@csrf_exempt
@login_required
def follow(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    user_id = data.get("user_id", "")
    userfollow = data.get("userfollow", False)  # Default to False if not provided

    print(user_id, userfollow)
    # Implement your follow/unfollow logic here
    # You can use 'user_id' and 'userfollow' to update your database accordingly

    # Example: If 'userfollow' is True, you can add a new follower; if False, you can remove the follower.

    # Return a success response
    return JsonResponse({"success": True})


# def follow(request, user_id):

#     if request.method == "POST":
#         already_follow = Follower.objects.filter(user=request.user, userfollow=user_id).exists()

#         # If the user is already followed do not create new follow entry and return to user page.
#         if already_follow:
#             return HttpResponseRedirect(reverse("user", args=[user_id]))
        
#         # If user is not followed creates new follow entry and returns to user page.
#         else:
#             try:
#                 Follower.create_follow(user=request.user, userfollow=user_id)
#             except IntegrityError:
#                 return render(request, "network/index.html", {
#                     "message": "Could not Follow User"
#                 })
#         return HttpResponseRedirect(reverse("user", args=[user_id]))

def index(request):

    allPost = Post.objects.all().order_by('-timeStamp')
    paginator = Paginator(allPost, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    has_previous_page = page_obj.has_previous
    
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

    return HttpResponseRedirect(reverse("index"))



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

def user(request, user_id):

    #Gets all needed info for profile page
    user_info = User.objects.filter(id = user_id).first()

    # Gets all post made by active user
    userPost = Post.objects.filter(user = user_info).order_by('-timeStamp')

    already_follow = Follower.objects.filter(user=request.user, userfollow=user_id).exists()


    paginator = Paginator(userPost, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    has_previous_page = page_obj.has_previous

    return render(request, "network/user.html",{
        "page_obj": page_obj,
        "user_info": user_info,
        "has_previous_page": has_previous_page,
        "already_follow": already_follow
    })