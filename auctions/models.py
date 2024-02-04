from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class ListingCategory(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    name = models.CharField(max_length=64)  # varchar(64)
    description = models.TextField(null=True)  # Text
    image = models.URLField(blank=True, null=True,
                            default='https://via.placeholder.com/500')  # Url
    category = models.ForeignKey(
        ListingCategory, on_delete=models.PROTECT, related_name='listings')  # FK references ListingCategory
    date = models.DateTimeField(default=datetime.now)

    current_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    starting_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=False)
    earliest_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)

    opened = models.BooleanField(default=True)

    made_by = models.ForeignKey(
        'User', on_delete=models.PROTECT, related_name='listings_made', null=True)

    def __str__(self):
        return f"{self.name}: ${self.current_price}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.current_price:
            self.current_price = self.starting_bid
            self.earliest_bid = self.starting_bid
        super().save(*args, **kwargs)


class User(AbstractUser):
    watchlist = models.ManyToManyField(AuctionListing)

    def __str__(self):
        return f"{self.username}"


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bids')
    auction_listing = models.ForeignKey(
        AuctionListing, on_delete=models.SET_NULL, related_name='bids', null=True)
    name = models.CharField(max_length=64, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    date = models.DateTimeField(default=datetime.now)
    BID_STATE = [
        ('W', 'Winning'),  # va ganando la subasta
        ('O', 'Outbid'),  # fue superado
        ('L', 'Lost'),  # perdio la subasta
        ('F', 'Final'),  # gano la subasta
    ]
    state = models.CharField(
        max_length=1, choices=BID_STATE, default='W')

    def save(self, *args, **kwargs):
        if not self.pk and not self.name:
            if self.auction_listing:
                self.name = self.auction_listing.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}: ${self.price}, on {self.date} ({self.state})"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    auction_listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(default=datetime.now)

    # TODO implementar sistema de replies
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.user.username}: {self.content}"
