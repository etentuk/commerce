from typing import List
from django.contrib import admin
from .models import Categories, Listing, User, WatchList


class ListingDisplay(admin.ModelAdmin):
    list_display = ("title", "category", "price", "created_at")


class WatchListDisplay(admin.ModelAdmin):
    list_display = ("item", "date_added")

    # Register your models here.
admin.site.register(Listing, ListingDisplay)
admin.site.register(Categories)
admin.site.register(User)
admin.site.register(WatchList, WatchListDisplay)
