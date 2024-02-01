from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import AuctionListing, ListingCategory

from .models import User


def index(request):
    return render(request, "auctions/index.html", {
        'listings': AuctionListing.objects.all().filter(opened=True),
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
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
        category = ListingCategory.objects.get(name=request.POST['category'])
        price = request.POST['starting-bid']

        if not name or not image or not category or not price:
            return render(request, 'auctions/create.html', {
                'required_fields': True,
                'message': 'Name and starting bid are required.',
                'categories': categories,
            })
        
        try:
            listing = AuctionListing.objects.create(
                name=name,
                description=description,
                image=image,
                category=category,
                current_price=price,
            )
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        except IntegrityError:
            return render(request, 'auctions/create.html', {
                'required_fields': False,
                'message': 'Name already taken,',
                'categories': categories,
            })

    return render(request, 'auctions/create.html', {
        'required_fields': False,
        'categories': categories,
    })


def show_listing(request, listing_id):
    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return render(request, 'auctions/error.html', {
            'message': 'Listing does not exist.',
        })

    return render(request, 'auctions/listing.html', {
        'listing': listing,
    })
