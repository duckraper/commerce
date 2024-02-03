from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class ListingCategory(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    name = models.CharField(max_length=64) # varchar(64)
    description = models.TextField(null=True) #Text
    image = models.URLField(blank=True) #Url
    category = models.ForeignKey(
        ListingCategory, on_delete=models.PROTECT, related_name='listings') #FK references ListingCategory
    date = models.DateTimeField(default=datetime.now)
    current_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False)
    opened = models.BooleanField(default=True)
    made_by = models.ForeignKey(
        'User', on_delete=models.PROTECT, related_name='listings_made', null=True)

    def __str__(self):
        return f"{self.name}: ${self.current_price}"


class User(AbstractUser):
    watchlist = models.ManyToManyField(AuctionListing)
 
    def __str__(self):
        return f"{self.username}"


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bids')
    auction_listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name='bids')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username}: ${self.price} ({self.date})"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    auction_listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f"{self.user.username}: {self.content}"
