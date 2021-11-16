from typing import List
from django.forms import ModelForm
from .models import Listing


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price',
                  'image_url', 'category', 'active']
