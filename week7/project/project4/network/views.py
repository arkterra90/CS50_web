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
from .utils import handle_post_like_creation, update_post_like_count



from .models import *

from django.http import JsonResponse

@login_required
def follow_page(request):

    user = request.user
    userFollows = Follower.objects.filter(user=user)
    userFollowList = []
    # userFollowPost = Post.objects.filter(user=userFollows.userfollow).order_by('-timestamp')
    for follwerId in userFollows:
        userFollowId = follwerId.userfollow
        userFollowList.append(userFollowId)

    followedUsers = User.objects.filter(id__in=userFollowList)
    allPost = Post.objects.filter(user__in=followedUsers).order_by('-timeStamp')
    paginator = Paginator(allPost, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    has_previous_page = page_obj.has_previous

     # Query to get post the user has already liked
    userLikes = PostLike.objects.filter(user=request.user.id, currentLike=True)
    userLikesPostId = []
    for likes in userLikes:
            likeId = likes.post
            userLikesPostId.append(likeId)

    # Need to make query to postlike model to count how many likes are available
    # for each post and send as a dictionary.
    
    return render(request, "network/follow.html", {
        "allPost": allPost,
        "page_obj": page_obj,
        "has_previous_page": has_previous_page,
        "userLikes": userLikesPostId
    })

    print(followedUserPost)
    
    return render(request, "network/follow.html")

# Allows a user to follow and unfollow other users using follow as an API route for AJAX request.
@csrf_exempt
@login_required
def follow(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    user_id = data.get("user_id", "")
    ifFollower = data.get("ifFollower", "")
    already_follow = Follower.objects.filter(user=request.user, userfollow=user_id)

    if ifFollower:
        try:
            # To prevent making duplicate model entries model is checked for previous follow of
            # user and if found currentFollow is changed to True to reflect users re-following of
            # user.
            if already_follow.exists():
                follower_instance = already_follow.first()
                follower_instance.currentFollow = True
                follower_instance.save()
                return JsonResponse({"success": "New Follow Created"})

            # if already_follow.exists() is none a new entry is added to the Follower model
            else:
                Follower.create_follow(user=request.user, userfollow=user_id, currentFollow=True)
                return JsonResponse({"success": "New Follow Created"})
        except IntegrityError:
            return JsonResponse({"error": "Could not create user follow record"})
        
    # If the user current follows the profile and clicks to unfollow the profile
    # the Follower model is changed to reflect the users desire to unfollow the profile.
    else:
        if already_follow.exists():
            follower_instance = already_follow.first()
            follower_instance.currentFollow = False
            follower_instance.save()
            return JsonResponse({"success": "Already a follower"})
        else:
            return JsonResponse({"error": "Not a follower"})

@login_required
@csrf_exempt
def like(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    
    data = json.loads(request.body)
    postId = data.get("postId", "")

    loggedinuser = request.user.id
    postExist = Post.objects.get(id=postId)
    alreadyLike = PostLike.objects.filter(post=postExist, user=loggedinuser)
    
    
    # Checks if logged in user is the same as the post creator user.
    postLike_instance = alreadyLike.first()

    if alreadyLike.exists():
        if postLike_instance.user == loggedinuser:
            postLike_instance.currentLike = not postLike_instance.currentLike
            postLike_instance.save()
            if postLike_instance.currentLike:
                update_post_like_count(postExist)
                return JsonResponse({"success": "post liked"})
            else:
                update_post_like_count(postExist)
                return JsonResponse({"success": "post unliked"})
        else:
            result = handle_post_like_creation(post=postExist, user=loggedinuser)
            update_post_like_count(postExist)
            return result

    # If user has never liked the post before, the user can like a post.
    else:
        result = handle_post_like_creation(post=postExist, user=loggedinuser)
        update_post_like_count(postExist)
        return result

    # Moved outside the if-else blocks
    


def index(request):

    # Query to get all post and paginate the post
    allPost = Post.objects.all().order_by('-timeStamp')
    paginator = Paginator(allPost, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    has_previous_page = page_obj.has_previous

    # Query to get post the user has already liked
    userLikes = PostLike.objects.filter(user=request.user.id, currentLike=True)
    userLikesPostId = []
    for likes in userLikes:
            likeId = likes.post
            userLikesPostId.append(likeId)


    # Need to make query to postlike model to count how many likes are available
    # for each post and send as a dictionary.
    
    return render(request, "network/index.html", {
        "allPost": allPost,
        "page_obj": page_obj,
        "has_previous_page": has_previous_page,
        "userLikes": userLikesPostId
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

    logInId = request.user.id
    print(logInId)
    if user_id == request.user.id:
        return render(request, "network/profile.html",{
            "page_obj": page_obj,
            "user_info": user_info,
            "has_previous_page": has_previous_page,
            "already_follow": already_follow
        })
    
    else:

        return render(request, "network/user.html",{
            "page_obj": page_obj,
            "user_info": user_info,
            "has_previous_page": has_previous_page,
            "already_follow": already_follow
        })