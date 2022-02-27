from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from .form import *
from .models import *

import urllib.parse

def index(request):
    #currentAuction = Bid.objects.values('auction').annotate(maxBid = Max('bid'))

    maxAuctions = Auction.objects.annotate(max_bid=Max('bids__bid')).order_by('-creationDate')


    return render(request, "auctions/index.html",
    {"auctions": maxAuctions,'watchCount': watchCount(request)})

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
        
    form = NewAuctionForm(request.POST or None)

    if form.is_valid():
        
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        startBid = form.cleaned_data['startBid']
        imageURL = form.cleaned_data['imageURL'] or ''
        category = form.cleaned_data['category'] or 'No Category Listed'

        newListing = Auction(
            title = title, 
            description = description,
            imageURL = imageURL, 
            category = category,
            seller = request.user,
            startBid = startBid
        )            

        openingBid = Bid(
            auction= newListing,
            bid = startBid,
            bidder = request.user
        )

        try:
            newListing.save()
            openingBid.save()
        except IntegrityError:
            return render(request, "auctions/newListing.html", {
                "message": "There was an issue posting your ad. Please try again", 'form':form,
                })
        return redirect(f"/auction/{newListing.pk}", {"message":"Success: Your auction is now live",})

    else:
        return render(request, "auctions/newListing.html", {'form':form,})

def auction(request, auction_id):
    # get current auction with highest current bid
    currentAuction = Auction.objects.filter(pk = auction_id).annotate(max_bid=Max('bids__bid')).get(pk=auction_id)
    currentBids = Bid.objects.filter(auction = currentAuction) # get the bids on the current auction
    maxBid = float(currentBids.aggregate(Max('bid'))['bid__max']) # get the maximum bid amount
    currentBid = currentBids.get(bid = maxBid) # get the current bid

    spanClass = 'far'

    # get auction comment
    comments = Comment.objects.filter(auction = auction_id).order_by('-creationDate')

    if request.user == 'AnonymousUser':
        if (isInWatchList(request, auction_id).count() == 0):
            spanClass = 'far'
        else:
            spanClass = "fas"

    if (request.user == currentBid.bidder):
        bidMessage = "You are the highest bidder"
    else:
        bidMessage = f"{currentBid.bidder} is the highest bidder"

    return render(request, "auctions/auction.html", {
        "auction": currentAuction,
        'watchCount': watchCount(request),
        'spanClass' : spanClass,
        'comments'  : comments,
        'bidForm'   : NewBidForm({ 'bid':round( maxBid,2 ) }),
        'bidMessage': bidMessage,
        'ended'     : currentAuction.hasEnded()
        })

@login_required(login_url='/login')
def categories(request, category = None):
    if category is not None:
        auctions = Auction.objects.filter(category = category)
        return render(request, f"auctions/index.html", {"auctions": auctions, "category": category})

    # get all the categories (without duplicate)    
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

@login_required(login_url='/login')
def comment(request):
    ''' return watchlist '''
    # get the current user from database
    currentUser = User.objects.filter(username = request.user).first()
    user = request.user.username
    # parse query
    queryStr = request.body.decode('utf-8')
    parsedQueryStr =  urllib.parse.parse_qs(queryStr)
    comment = parsedQueryStr['comment'][0]
    auction_id = int(parsedQueryStr['auction_id'][0])
    
    currentAuction = Auction.objects.get(id=auction_id)

    Comment(auction = currentAuction, comment = comment, user = currentUser).save()

    return JsonResponse({ 'comment': 'valid', 'user': user })

@login_required(login_url='/login')
def bid(request):

    if request.method == 'POST':
        query = request.POST
        auction_id = query.get('auction_id')
        currentAuction = Auction.objects.get(id = auction_id)

        if currentAuction.hasEnded():
            return auction(request, auction_id)
            
        currentBid = float(query.get('bid'))
        currentMaxBid = float(Auction.objects.filter(pk = auction_id).annotate(max_bid=Max('bids__bid')).get(pk=auction_id).max_bid)

        currentUser = User.objects.get(username = request.user)
        currentWinningBid = Bid.objects.filter(auction_id = currentAuction)
        currentWinningBidder = currentWinningBid.get(bid = currentMaxBid).bidder
        
        if  request.user != currentWinningBidder: # no need for the winning bidder to bid again if already winning
            if currentBid <= currentMaxBid:
                return JsonResponse({'bidMessage':'Your bid is too low','winningBid':currentMaxBid})
            if currentBid > currentMaxBid:
                newBid = Bid(
                    auction = currentAuction,
                    bid = currentBid,
                    bidder = currentUser)

                newBid.save()

                return JsonResponse({'bidMessage':'You are the highest bidder', 'winningBid':currentBid})

    return JsonResponse({'bidMessage':'You are already the highest bidder', 'winningBid':currentMaxBid})

@login_required(login_url='/login')
def endAuction(request, auction_id):

    if request.method=='POST':
        currentAuction = Auction.objects.get(id = auction_id)
        if request.user == currentAuction.seller:
            currentAuction.endAuction()
            currentAuction.save()
    
    return auction(request, auction_id)