from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User
from .models import Auctions, Category, Watch, Bid, Comments
from .forms import AddListings, AddCategory, PlaceBid, AddComment

# List of all Categories on this app

product_categories = [ 'Fashion',
    'Electronics',
    'Toys',
    'Men',
    'Women',
    'Children',
    'Shoes',
    'Furniture',
    'Clothing',
    'Hair',
    'Watches']

# View function to show all active listings    

def index(request):
    auctions = Auctions.objects.order_by("-date_created").filter(is_closed=False)
    categories = product_categories
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "categories": categories,
        "active1": "active"
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

        if not username or not email or not password:
            return render(request, "auctions/register.html", {
                "message": "Kindly ensure you fill all fields."
            })
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

# View function to create a listing

def createListing(request):

    # User can create a listing if logged in
    if request.user.is_authenticated:
        categories = product_categories

        if request.method == "POST":
            listform = AddListings(request.POST)
            catform = AddCategory(request.POST)
            if listform.is_valid() and catform.is_valid():
                titl = listform.cleaned_data["titl"]
                prod = listform.cleaned_data["prod"]
                cat = catform.cleaned_data["cat"]
                desc = listform.cleaned_data["desc"]
                amount = listform.cleaned_data["amount"]

                # Ensure either jpg, webp, jpeg and png as image extension
                if prod != None and "jpg" in prod:
                    p = Auctions.objects.create(title=titl, product=prod, price=amount, description=desc, seller=request.user)
                elif prod != None and "webp" in prod:
                    p = Auctions.objects.create(title=titl, product=prod, price=amount, description=desc, seller=request.user)
                elif prod != None and "jpeg" in prod:
                    p = Auctions.objects.create(title=titl, product=prod, price=amount, description=desc, seller=request.user)
                elif prod != None and "png" in prod:
                    p = Auctions.objects.create(title=titl, product=prod, price=amount, description=desc, seller=request.user)        
                else:
                    p = Auctions.objects.create(title=titl, price=amount, description=desc, seller=request.user)

                # Check if the category picked by user is already in the Category Models
                for c in cat:
                    result = Category.objects.filter(product_category=c).exists()

                    # If it is, do not create 
                    if result == True:
                        ptr = Category.objects.get(product_category=c)
                        ptr.auctio.add(p)
                    # else create    
                    else:
                        ptr = Category.objects.create(product_category=c)
                        ptr.auctio.add(p)
            return HttpResponseRedirect(reverse("index"))
        else:            
            return render(request, "auctions/createListing.html", {
                "form1": AddListings(),
                "form2": AddCategory(),
                "categories": categories,
                "active2": "active"
            })
    # if user is not logged in and clicks the create list link, user should be taken to login form         
    else:
        return render(request, "auctions/login.html")

def page(request, auction_id):
    categories = product_categories

    # User can go to a listing page if logged in
    if request.user.is_authenticated:
        message = "Bid must be higher than current bid"
        auc = Auctions.objects.get(pk=auction_id)
        result = Watch.objects.filter(watch_product=auc, watch_user=request.user).exists()
        num = Bid.objects.filter(item=auc).count()

        # Add items to watchlist
        if request.method == "POST" and 'add' in request.POST:
            Watch.objects.create(watch_product=auc, watch_user=request.user)
            # return HttpResponseRedirect(reverse("watch"))
            return HttpResponseRedirect(reverse("page", kwargs={'auction_id': auction_id }))

        # Remove items from watchlist    
        elif request.method == "POST" and 'remove' in request.POST:
            Watch.objects.get(watch_product=auc, watch_user=request.user).delete()
            # return HttpResponseRedirect(reverse("watch"))
            return HttpResponseRedirect(reverse("page", kwargs={'auction_id': auction_id }))

        # Place bid on items    
        elif request.method == "POST" and 'place' in request.POST:
            bidform = PlaceBid(request.POST)
            if bidform.is_valid():
                curPrice = bidform.cleaned_data["curPrice"]
                if auc.price < curPrice:
                    auc.price = curPrice
                    auc.save()
                    Bid.objects.create(item=auc, buyer=request.user, bidPrice=curPrice)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    messages.error(request, 'Bid must be higher than current bid')
                    return redirect("page", auction_id = auc.id )

        # Close listing            
        elif request.method == "POST" and 'close' in request.POST:
            auc.is_closed = True
            auc.save()
            return HttpResponseRedirect(reverse("index"))

        # Comment on listings    
        elif request.method == "POST" and 'comment' in request.POST:
            commentform = AddComment(request.POST)
            if commentform.is_valid():
                comment = commentform.cleaned_data["comments"]
                Comments.objects.create(listing=auc, comment=comment, user=request.user)
            return HttpResponseRedirect(reverse("page", kwargs={'auction_id': auc.id }))

        # GET request of listing page
        else:
            bidforitem = Bid.objects.filter(item=auc)
            comments = Comments.objects.order_by("-timestamp").filter(listing=auc)

            # Check for listing winner
            if bidforitem:
                price = Bid.objects.filter(item=auc).order_by('-id')[0]
                winprice = price.bidPrice
                person = Bid.objects.get(item=auc, bidPrice=winprice)
                winner = person.buyer
            else:
                winner = None
            return render(request, "auctions/page.html", {
                "auction": auc,
                "form": PlaceBid(),
                "form2": AddComment(),
                "winner": winner,
                "result": result,
                "number": num,
                "comments": comments,
                "categories": categories,
                "active3": "active"
            })

    # if user is not logged in and clicks on a listing, user should be taken to login form         
    else:
        return render(request, "auctions/login.html")    

# View function for watchlist
def watch(request):

    # User can go to their watchlist if logged in
    if request.user.is_authenticated:
        categories = product_categories
        user = User.objects.get(username=request.user)
        watchs = Watch.objects.filter(watch_user=user)

        return render(request, "auctions/watchlist.html", {
            "watchs": watchs,
            "categories": categories,
            "active4": "active"
        })
    # if user is not logged in and clicks on watchlist navigation link, user should be taken to login form      
    else:
         return render(request, "auctions/login.html")

@login_required
def remove_watch(request, auction_id):

    auc = Auctions.objects.get(pk=auction_id)
    # Remove items from watchlist    
    if request.method == "POST" and 'remove' in request.POST:
        Watch.objects.get(watch_product=auc, watch_user=request.user).delete()
        return HttpResponseRedirect(reverse("watch"))


# View function to display all categories
def category(request):
    categories = product_categories
    return render(request, "auctions/categories.html", {
        "categories": categories,
        "active6": "active"
    })

# View function to display all listings in a particular category
@login_required
def catlist(request, list_id):
    categories = product_categories
    category = Category.objects.get(pk=list_id)
    products = category.auctio.order_by("-date_created").filter(is_closed=False)
    return render(request, "auctions/catlist.html", {
        "products": products,
        "categories": categories,
        "active5": "active"
    })

# View function to get the category primary key and redirect to CATLIST view function
@login_required
def get_category(request, category):
    categories = product_categories
    if Category.objects.filter(product_category=category).exists() == True:
        thecategory = Category.objects.get(product_category=category)
        return HttpResponseRedirect(reverse("catlist", kwargs={'list_id': thecategory.id }))
    else:
        return render(request, "auctions/categories.html", {
            "check": "nothing",
            "categories": categories
        })

# View function for searching by category
def search(request):
    value = request.GET['q']
    captalizedValue = value.capitalize()
    result = Category.objects.filter(product_category=captalizedValue).exists()
    categories = product_categories
    all_categories = Category.objects.all()
    cat_search = []
    if result == True:
        category = Category.objects.get(product_category=captalizedValue)
        cat_search.append({"id": category.id, "product": category.product_category})
        return render(request, "auctions/searchresult.html", {
            "results": cat_search,
            "categories": categories
        })
    else:
        for category in all_categories.iterator():
            if value.lower() in category.product_category.lower(): 
                cat_search.append({"id": category.id, "product": category.product_category})
        if len(cat_search) == 0:
            return render(request, "auctions/searchresult.html", {
            "check": "None",
            "categories": categories
        })
        else:
            return render(request, "auctions/searchresult.html", {
            "results": cat_search,
            "categories": categories
        })
 
    






