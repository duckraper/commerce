from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import AuctionListing, ListingCategory

from .models import User


def index(request):
    auction_listing = AuctionListing.objects.all().filter(opened=True)
    if request.user.is_authenticated:
        user_watchlist = [
            listing for listing in auction_listing if listing in request.user.watchlist.all()]
        print(user_watchlist)
        return render(request, 'auctions/index.html', {
            'listings': auction_listing,
            'watchlist': user_watchlist,
        })

    return render(request, "auctions/index.html", {
        'listings': auction_listing,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(  # type: ignore
                username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def create_listing(request):
    categories = ListingCategory.objects.all()

    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        image = request.POST['image']
        category_name = request.POST['category']
        price = request.POST['starting-bid']

        if not (name and image and category_name and price):
            return render(request, 'auctions/create.html', {
                'message': 'Make sure of filling at least the fields: name, image, category, and starting bid properly.',
                'categories': categories,
            })

        try:
            _category = ListingCategory.objects.get(name=category_name)
            listing = AuctionListing.objects.create(
                name=name,
                description=description,
                image=image,
                category=_category,
                starting_bid=price,
                made_by=request.user
            )
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        except ListingCategory.DoesNotExist:
            return render(request, 'auctions/create.html', {
                'message': 'Category does not exist.',
                'categories': categories,
            })

    return render(request, 'auctions/create.html', {
        'categories': categories,
    })


@login_required(login_url='login')
def delete_listing(request, listing_id):
    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return render(request, 'auctions/error.html', {
            'message': 'Listing does not exist.',
        })

    listing.delete()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='login')
def edit_listing(request, listing_id):
    categories = ListingCategory.objects.all()

    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return render(request, 'auctions/error.html', {
            'message': 'Listing does not exist.',
        })

    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        image = request.POST['image']
        category_name = request.POST['category']
        price = request.POST['starting-bid']

        if not (name and image and category_name and price):
            return render(request, 'auctions/create.html', {
                'message': 'Make sure of filling at least the fields: name, image, category, and starting bid properly.',
                'categories': categories,
            })

        try:
            _category = ListingCategory.objects.get(name=category_name)
            listing.name = name
            listing.description = description
            listing.image = image
            listing.category = _category
            listing.current_price = price
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))

        except ListingCategory.DoesNotExist:
            return render(request, 'auctions/create.html', {
                'message': 'Category does not exist.',
                'categories': categories,
            })

    return render(request, 'auctions/edit.html', {
        'listing': listing,
        'categories': categories,
    })


def show_listing(request, listing_id):
    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return render(request, 'auctions/error.html', {
            'message': 'Listing does not exist.',
        })

    # si se hizo algun bid
    if request.method == "POST":
        bid = float(request.POST['bid'])

        if bid <= listing.current_price:
            return render(request, 'auctions/listing.html', {
                'message': 'Price must be greater than the current price.',
            })

        listing.current_price = bid  # type: ignore
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))

    return render(request, 'auctions/listing.html', {
        'listing': listing,
    })


def show_categories(request):
    return render(request, 'auctions/categories.html', {
        'categories': ListingCategory.objects.all(),
    })


def show_my_bids(request):
    return render(request, 'auctions/my_bids.html', {
        'bids': request.user.bids.all(),
    })

def show_category(request, category_id: int):
    try:
        category = ListingCategory.objects.get(pk=category_id)
        listing_list = category.listings.all()  # type: ignore

    except ListingCategory.DoesNotExist:
        return render(request, 'auctions/error.html', {
            'message': 'Category does not exist.',
        })

    return render(request, 'auctions/category.html', {
        'category': category,
        'listings': listing_list,
    })


@login_required(login_url='login')
def show_watchlist(request):
    return render(request, 'auctions/watchlist.html', {
        'watchlist': request.user.watchlist.all(),
    })


@login_required(login_url='login')
def show_my_listings(request):
    return render(request, 'auctions/my_listings.html', {
        'listings': request.user.listings_made.all(),
    })


def bid(request, listing_id):
    if request.method == "POST":
        try:
            listing = AuctionListing.objects.get(pk=listing_id)
        except AuctionListing.DoesNotExist:
            return render(request, 'auctions/error.html', {
                'message': 'Listing does not exist.',
            })

        price = request.POST['bid']

        if price <= listing.current_price:
            return render(request, 'auctions/error.html', {
                'message': 'Price must be greater than the current price.',
            })

        listing.current_price = price
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))


# TODO implement comment view
@login_required(login_url='login')
def comment(request, listing_id):
    return redirect(request, 'auctions/comment.html', {
        'listing': AuctionListing.objects.get(pk=listing_id),
    })
