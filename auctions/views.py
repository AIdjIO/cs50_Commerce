from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from .form import *
from .models import *

def index(request):
    print(Auction.objects.all())
    return render(request, "auctions/index.html",
    {"auctions": Auction.objects.all(),'watchCount': watchCount(request)})

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

@login_required(login_url='/login')
def newListing(request):
    if request.method == 'POST':
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            startBid = form.cleaned_data['startBid']
            imageURL = form.cleaned_data['imageURL'] or ''
            category = form.cleaned_data['category'] or 'No Category Listed'

            newListing = Auction(
                title = title, 
                description = description, 
                startBid = startBid, 
                imageURL = imageURL, 
                category = category,
                seller = request.user
            )

            try:
                newListing.save()
            except IntegrityError:
                return render(request, "auctions/newListings.html", {
                    "message": "There was an issue posting your ad. Please try again"
                })
            return redirect(f"auction/{newListing.pk}", {"message":"Success: Your auction is now live"})
    else:
        return render(request, "auctions/newListing.html", {'form': NewAuctionForm()})

@login_required(login_url='/login')
def auction(request, auction_id):
    auction = Auction.objects.get( pk = auction_id )
    if (isInWatchList(request, auction_id).count() == 0):
        spanClass = 'far'
    else:
        spanClass = "fas"

    return render(request, "auctions/auction.html", {"auction": auction, 'watchCount': watchCount(request), 'spanClass' : spanClass})

@login_required(login_url='/login')
def categories(request, category = None):
    if category is not None:
        auctions = Auction.objects.filter(category = category)
        return render(request, f"auctions/index.html", {"auctions": auctions, "category": category})    
    categories = Auction.objects.values('category').distinct().order_by("category")
    return render(request, f"auctions/category.html", {"categories": categories})

def isInWatchList(request, auction_id):
    ''' return whether an auction is in the watch list '''
    # auction_id = int(request.body.decode('utf-8'))
    currentUser = User.objects.get(username = request.user)
    currentAuction = Auction.objects.get(id=auction_id)
    
    # get the user watch list
    userWatchList = WatchList.objects.filter(watcher = currentUser.id, watching = auction_id)
    # # check if current listing in user watchlist
    # listingInWatchList = userWatchList.filter(watching = auction_id)
    return userWatchList


def watchCount(request):
    ''' return the number of listing in user watch list  '''
    if request.user.is_authenticated:
        #get current user
        currentUser = User.objects.get(username = request.user)
        # get the user watch list
        userWatchList = WatchList.objects.filter(watcher = currentUser.id)
        # get total listing in watchlist
        return userWatchList.count()
    else: return None

@login_required(login_url='/login')
def updateWatchList(request):
    ''' Update watch list '''
    auction_id = int(request.body.decode('utf-8'))
    currentUser = User.objects.get(username = request.user)
    currentAuction = Auction.objects.get(id=auction_id)

    if isInWatchList(request, auction_id).count() == 0 :
        WatchList(watching = currentAuction, watcher = currentUser).save()
        spanClass = "fas" #fontAwesome class for solid icon
    else:
        isInWatchList(request, auction_id).delete()
        spanClass = "far" #fontAwesome class for regular icon

    return JsonResponse({'total': watchCount(request), 'spanClass': spanClass})

@login_required(login_url='/login')
def watchList(request):
    ''' return watchlist '''
    # get the current user
    currentUser = User.objects.filter(username = request.user).first()
    # get the user watch list
    userWatchList = WatchList.objects.filter(watcher_id = currentUser.id)

    auctions = [c.watching for c in userWatchList]

    return render(request, "auctions/index.html", 
    {"auctions": auctions, 'watchCount': watchCount(request)
    })