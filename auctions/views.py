from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models.aggregates import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CommentForm, ListingForm
from django.core.exceptions import ObjectDoesNotExist

from .models import Categories, Listing, User, WatchList, Bid


def index(request):
    listings = Listing.objects.exclude(active=False).all
    return render(request, "auctions/listings_display.html", {
        "listings": listings,
        "title": "Active Listings"
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


@login_required(login_url='/login')
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.owner = request.user
            new_listing.save()
            return HttpResponseRedirect(reverse("listing", args=[new_listing.id]))
    return render(request, "auctions/create_listing.html", {
        "form": ListingForm
    })


def listing(request, listing_id):
    listing = None
    added = None
    current_price = 0
    message = ""
    winner = False

    if request.method == 'POST' and request.user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        max_bid = listing.bids.aggregate(Max('bid_price'))['bid_price__max']
        placed_bid = int(request.POST['bid_price'])
        listing_price = int(max_bid or 0) or listing.price

        if((listing_price == listing.price) and not max_bid and placed_bid < listing_price):
            message = 'Bid must be greater or equal to current value'
        elif(placed_bid < listing.price and max_bid):
            message = 'Bid must be greater than current price'
        else:
            listing.price = placed_bid
            listing.save()
            Bid.objects.create(bid_price=placed_bid,
                               owner=request.user, listing=listing)

    try:
        listing = Listing.objects.get(pk=listing_id)
    except ObjectDoesNotExist:
        listing = None
    else:
        current_price = int(listing.bids.aggregate(Max('bid_price'))[
            'bid_price__max']) or listing.price
        try:
            if(listing.active == False and listing.bids.order_by('-bid_price')[0].owner == request.user):
                winner = True
        except IndexError:
            winner = False
        else:
            winner = False
        comments = listing.comments.all()
    try:
        if(request.user.is_authenticated):
            added = listing.watchlist_items.get(owner=request.user)
        else:
            added = None
    except ObjectDoesNotExist:
        added = None

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": added,
        "winner": winner,
        "current_price": current_price,
        "message": message,
        "current_user": request.user == listing.owner,
        "comment_form": CommentForm(),
        "comments": comments,
        "authenticated": request.user.is_authenticated,
    })


def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@ login_required(login_url='/login')
def watchlist_action(request, action, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    match action:
        case 'add':
            WatchList.objects.create(
                item=listing, owner=request.user)
        case 'remove':
            WatchList.objects.filter(owner=request.user, item=listing).delete()
        case _:
            return
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@ login_required(login_url='/login')
def create_comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    form = CommentForm(request.POST)
    print(request.POST)
    if(form.is_valid):
        comment = form.save(commit=False)
        comment.listing = listing
        comment.owner = request.user
        comment.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@ login_required(login_url='/login')
def watchlist(request):
    watchlist_listings = request.user.watchlist_items.all()
    listings = []
    for listing in watchlist_listings.all():
        listings += [listing.item]
    return render(request, "auctions/listings_display.html", {
        "listings": listings,
        "title": "Watchlist"
    })


def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_page(request, category_id):
    category = Categories.objects.get(pk=category_id)
    return render(request, "auctions/listings_display.html", {
        "listings": category.listings.all(),
        "category": category.name,
        "title": "Category"
    })
