from typing import List
from django.forms import ModelForm
from .models import Bid, Listing


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price',
                  'image_url', 'category', 'active']


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_price']
