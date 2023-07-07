from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .forms import *

# Loads index page and sends all data from listing model to 
# show user only active listings.
def index(request):
    return render(request, "auctions/index.html", {
        "listing": Listing.objects.filter(list_active=True)
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(redirect_field_name='index')    
def list_add(request):
    if request.method == "POST":
        if 'save' in request.POST:
            f = ListingForm(request.POST)
            if f.is_valid():
                instance = f.save(commit=False)
                instance.list_user = request.POST.get('list_user')
                instance.save()
                return render(request, "auctions/index.html")
            else:
                return render(request, "auctions/list_add.html", {
                    "message": "Listing was not saved",
                    "ListingForm": ListingForm
                })
        if 'add' in request.POST:
            f = ListingForm(request.POST)
            if f.is_valid():
                instance = f.save(commit=False)
                instance.list_user = request.POST.get('list_user')
                instance.save()
                return render(request, "auctions/list_add.html", {
                    "ListingForm": ListingForm
                })
            else:
                return render(request, "auctions/list_add.html", {
                    "message": "Listing was not saved",
                    "ListingForm": ListingForm
                })
    else:
        return render(request, "auctions/list_add.html", {
            "ListingForm": ListingForm
        })
    

@login_required(redirect_field_name='index')    
def list_view(request, list_id):
    list_item = Listing.objects.get(pk=list_id)
    
    # For a brand new item there will not be comments or bids so a
    # try/except is needed to handle for errors with the query.
    try:
        list_bid = bids.objects.get(pk=list_id)
    except (NameError, ObjectDoesNotExist):
        list_bid = None
    
    try:
        list_comment = comments.objects.filter(item=list_item)
    except (NameError, ObjectDoesNotExist):
        list_comment = None

    print(list_comment)
    return render(request, "auctions/list_view.html",{
        "list_item": list_item,
        "BidForm": bidsForm,
        "CommentsForm": CommentsForm, 
        "list_bid": list_bid,
        "list_comment": list_comment
    })

def item_comments(request, list_id):
    listing = Listing.objects.get(pk=list_id)
    f = CommentsForm(request.POST)
    if f.is_valid:
        instance = f.save(commit=False)
        instance.user_comment = request.POST.get('bid_user')
        instance.item = listing
        instance.save()
        return HttpResponseRedirect(reverse("list_view", args=(listing.id,)))