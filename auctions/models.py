from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET


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
