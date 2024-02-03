from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("my_listings", views.show_my_listings, name="my_listings"),
    path("categories", views.show_categories, name="categories"),
    path("my_bids", views.show_my_bids, name="my_bids"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("edit/<int:listing_id>", views.edit_listing, name="edit"),
    path("delete/<int:listing_id>", views.delete_listing, name="delete"),
    path("listing/<int:listing_id>", views.show_listing, name='listing'),
    path("category/<int:category_id>", views.show_category, name='category'),
    path("comment/<int:listing_id>", views.comment, name='comment'),
]
