from msilib.schema import ListBox
from queue import Empty
from telnetlib import STATUS
from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Watchlist, Comment
from .forms import NewListingForm, BidForm, CommentForm, CATEGORY_CHOICES


def index(request):
    current_user = request.user

    # try and give a badge for watchlist
    try:
        badge = Watchlist.objects.filter(
        added_by=current_user, watchlist__status=True).count()
    except:
        badge = 0
    
    listings=Listing.objects.filter(status=True).all()

    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_badge": badge
    })


def category(request,category):
    current_user = request.user

    # try and give a badge for watchlist
    try:
        badge = Watchlist.objects.filter(
        added_by=current_user, watchlist__status=True).count()
    except:
        badge = 0
    # listing filtered by category
    listings=Listing.objects.filter(status=True,category=category).all()

    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_badge": badge
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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):

    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            category = form.cleaned_data['category']
            image_url = form.cleaned_data['image_url']
            obj = Listing(
                title=title,
                description=description,
                price=price,
                category=category,
                image_url=image_url
            )
            obj.save()

            return HttpResponseRedirect(reverse("index"))
        else:

            return render(request, "auctions/create.html", {
                "form": NewListingForm
            })
    else:
        return render(request, "auctions/create.html", {
            "form": NewListingForm
        })


def listing(request, id):
    # make a context dictionary to dispatch various data
    current_user = request.user
    listing = Listing.objects.get(pk=id)
    all_comments = listing.commented_on.all()
    all_bids = listing.bids.all()
    total_bids = all_bids.count()
    created_by = listing.created_by

    # try give the badge for watchlist
    try:
        badge = Watchlist.objects.filter(
        added_by=current_user, watchlist__status=True).count()
    except:
        badge = 0

    # check whether the listing is added to watchlist or not
    if Watchlist.objects.filter(watchlist=listing).count() >= 1:
        button_name = "Remove from Watchlist"
    else:
        button_name = "Add to watchlist"

    # give a badge if item is in the watchlist
    if Watchlist.objects.filter(watchlist=listing).count() >= 1:
        watchlist_tag = "Watchlist"
    else:
        watchlist_tag = ""

    # check if the signed in user is same as the creator
    if created_by == current_user:
        is_creator = True
    else:
        is_creator = False

    context = {
        "button_name": button_name,
        "watchlist_badge": badge,
        "total_bids": total_bids,
        "listing_tag": watchlist_tag,
        "data": listing,
        "form": BidForm,
        "comments": all_comments,
        "comment_form": CommentForm,
        "total_bids": total_bids,
        "is_creator": is_creator
    }
    # setup forms for the listing page
    form = BidForm(request.POST)
    comment_form = CommentForm(request.POST)
    # check if a button is clicked
    if request.method == "POST":
        # checking if the "place bid" button is clicked
        if 'place_bid' in request.POST:
            if form.is_valid():
                amount = form.cleaned_data['amount']
                amounts = []
                for bid in all_bids:
                    amounts.append(bid.amount)
                try:
                    min_value = max(amounts)
                except:
                    min_value = listing.price
                # checking if the bid amount is higher than the price and previous bids
                if amount > min_value:

                    obj = Bid(
                        amount=amount,
                        listing=listing,
                        bid_by=current_user.username
                    )
                    obj.save()
                else:
                    # giving an error message if the price is lower than the min value
                    if listing.price >= amount:
                        message = "The value should atleast be higher than the starting price"
                    else:
                        message = "There is already a higher bid, you have to bid a bit more"

                    return render(request, "auctions/error.html", {"message": message})
                # returning to home page if the bid was successful
                return HttpResponseRedirect(reverse("index"), context)

        # check if "close" button is clicked and declare a winner
        elif 'close_listing' in request.POST:
            amounts = []
            bidders = []
            for bid in all_bids:
                amounts.append(bid.amount)
                bidders.append(bid.bid_by)
            try:
                max_value = max(amounts)
                winner = bidders[amounts.index(max_value)]
            except:
                max_value = listing.price
                winner = created_by.username

            listing.won_by = winner
            listing.status = False
            listing.save()

            return HttpResponseRedirect(reverse("index"), context)

        # check if a comment is submitted
        elif 'add_comment' in request.POST:
            if comment_form.is_valid():
                comment = comment_form.cleaned_data['comment_desc']

                obj = Comment(
                    comment_desc=comment,
                    commented_on=listing,
                    commentor=current_user.username
                )
                obj.save()
                return HttpResponseRedirect(reverse("listing",args=(id,)))
            else:
                context["message"]="Something didnt work while submitting comment"
                return render(request, "auctions/error.html", context)
        
        # add or remove watchlist
        elif 'add_to_watchlist' in request.POST:
            item = Watchlist.objects.filter(watchlist=listing)
            if item.count() >= 1:
                    item.delete()
                    return HttpResponseRedirect(reverse("index"), context)
            else:
                obj = Watchlist(
                        watchlist=listing,
                        added_by=current_user
                    )
                obj.save()
                return HttpResponseRedirect(reverse("index"), context)
        
        else:
            context["message"]="Something didnt work"
            return render(request, "auctions/error.html", context)

    else:
        # render all comments
        # check if the signed in user is a winner
        if listing.won_by == current_user.username:
            context["winning_message"] = "You Won!!"
            return render(request, "auctions/listing.html", context)
        else:
            return render(request, "auctions/listing.html", context)


def watchlist(request):
    current_user = request.user
    filtered_list = Watchlist.objects.filter(
        added_by=current_user, watchlist__status=True)
    badge = filtered_list.count()
    return render(request, "auctions/watchlist.html", {
        "watchlist_badge": badge,
        "listings": filtered_list
    })

def categories(request):
    categories=[]
    for cat in CATEGORY_CHOICES:
        categories.append(cat[0])

    return render(request, "auctions/categories.html", {"categories":categories})