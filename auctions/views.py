from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ListingForm
from django.core.exceptions import ObjectDoesNotExist

from .models import Listing, User, WatchList


def index(request):
    listings = Listing.objects.exclude(active=False).all
    return render(request, "auctions/index.html", {
        "listings": listings
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


@login_required(redirect_field_name='login')
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
    try:
        listing = Listing.objects.get(pk=listing_id)
    except ObjectDoesNotExist:
        listing = None
    try:
        added = listing.watchlist_items.get(owner=request.user)
    except ObjectDoesNotExist:
        added = None

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": added, })


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
