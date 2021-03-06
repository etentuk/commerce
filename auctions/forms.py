from typing import List
from django.forms import ModelForm
from .models import Bid, Comment, Listing


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price',
                  'image_url', 'category', 'active']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'comment']
