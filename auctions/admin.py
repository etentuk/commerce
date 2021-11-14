from typing import List
from django.contrib import admin
from .models import Categories, Listing, User

# Register your models here.
admin.site.register(Listing)
admin.site.register(Categories)
admin.site.register(User)
