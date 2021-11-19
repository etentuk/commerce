from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET, SET_DEFAULT
from django.db.models.expressions import Case


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(
        'Categories', blank=True, null=True, on_delete=SET(""), related_name='listings')
    owner = models.ForeignKey(
        User, on_delete=CASCADE, related_name="listings"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.category}"


class Categories(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class WatchList(models.Model):
    item = models.ForeignKey(
        Listing, on_delete=CASCADE, related_name='watchlist_items')
    owner = models.ForeignKey(
        User, on_delete=CASCADE, related_name='watchlist_items')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.item}"


class Bid(models.Model):
    bid_price = models.IntegerField()
    owner = models.ForeignKey(
        User, on_delete=CASCADE, related_name='bids')
    listing = models.ForeignKey(
        Listing, on_delete=CASCADE, related_name='bids'
    )
    date_placed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} - {self.bid_price}"
