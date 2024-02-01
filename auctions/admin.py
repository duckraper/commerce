from django.contrib import admin
from .models import User, AuctionListing, ListingCategory, Bid, Comment

# Register your models here.


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'category',
                    'date', 'current_price', 'opened')


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('wishlist',)


class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction_listing', 'price', 'date')


admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(ListingCategory)
admin.site.register(Comment)
