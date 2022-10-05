from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,ListingForm,Category,Listing,BidForm,CommentForm,Bid,Comment
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# import pdb; pdb.set_trace()

img_placeholder = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/681px-Placeholder_view_vector.svg.png"

def index(request,*arg):
    actives = Listing.objects.filter(is_active=True)
    cat=wl=None
    if arg:
        if arg[0][1]=='cat':
            cat=arg[0][0]
            category = Category.objects.get(name=cat)
            actives = actives.filter(category=category)
        else:
            wl=True
            actives = arg[0]
    for item in actives:
        x=item.description
        if len(x)>80:
            item.description = x[:77]+"..."
        if not item.img:
            item.img = img_placeholder
        item.curr_bid = round(item.curr_bid)
    return render(request, "auctions/index.html",{
        "listings":actives,
        "cat":cat,"wl":wl
    })

def login_view(request):
    """User login_page."""
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/login.html", {
            "message": "Invalid username and/or password."
        })
    return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    """New user registration page."""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation and not field is left blank.
        password = request.POST["password"]
        try:
            validate_password(password, username)
        except ValidationError as e:
            return render(request, "auctions/register.html", {"message":e})
        confirmation = request.POST["confirmation"]
        x_check = password != confirmation
        d_check = email and password and username
        if not d_check or x_check:
            message = "Atleast one field is empty."
            if x_check:
                message = "Passwords must match."
            return render(request, "auctions/register.html", {
                "message": message
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
    return render(request, "auctions/register.html")
    
def listing(request,lid):
    listing = Listing.objects.get(pk=lid)
    is_active = listing.is_active 
    cur_user = request.user
    same = listing.user==cur_user
    is_wl = cur_user in listing.watch_list.all()
    alert_color = "warning"
    message=None
    try:
        is_bid = Bid.objects.get(item=lid)
    except (Bid.DoesNotExist):
        is_bid = None
    if request.method == "POST":
        # Bidding logic
        bid = request.POST.get('new_bid',False)
        if bid and not same:
            bid = float("{:.2f}".format(float(bid)))
            if (not is_bid and bid>=listing.curr_bid) or bid>listing.curr_bid:
                if is_bid: is_bid.delete()
                new_bid = Bid(user=cur_user,item=listing,new_bid=bid)
                is_bid=new_bid
                new_bid.save()
                listing.curr_bid=bid
                listing.save()
            elif is_bid: message = "You must bid a value greater than the price."
            else: message = "You must bid a value equal to or greater than the price."
        # Comment logic
        comment = request.POST.get('comment',False)
        if comment:
            comment = Comment(user=cur_user,item=listing,comment=comment)
            comment.save()
        # Watch_list
        wl = request.POST.get('watch_list',False)
        if wl:
            if is_wl:
                listing.watch_list.remove(cur_user)
                is_wl=False
            else:
                listing.watch_list.add(cur_user)
                is_wl=True
        # closing listing
        if request.POST.get('close',False):
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse('index'))
    # GET    
    comments = Comment.objects.filter(item=lid)
    if not listing.img:
        listing.img= img_placeholder
    listing.curr_bid="{:.2f}".format(listing.curr_bid)
    if not listing.is_active:
        if cur_user==is_bid.user:
            message="You have won this bid."
            alert_color="success"
    return render(request, "auctions/listing.html",{
        "listing":listing,
        "title":listing.title.capitalize(),
        "form_bid":BidForm,"form_comment":CommentForm,
        "comments":comments,"same":same,"bid":is_bid,
        "is_active":is_active,"wl":is_wl,"message":message,
        "alert_color":alert_color
    })
    
@login_required
def new_listing(request):
    if request.method == "POST":
        my_querydict = request.POST.copy()
        my_querydict['user'] = request.user
        form = ListingForm(my_querydict)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.curr_bid="{:.2f}".format(instance.curr_bid)
            instance.title = instance.title.capitalize()
            instance.save()
            return  HttpResponseRedirect(reverse('index'))
        return render(request, "auctions/newlisting.html", {
                "message" : "Illegal entry.",
                "form": form
            })
    return render(request, "auctions/newlisting.html",{
                "form": ListingForm
        })

@login_required
def watch_list(request):
    cur_user = request.user
    watch_list = cur_user.listings.all()
    return index(request,watch_list)   

def categories(request):
    cats = Category.objects.all().order_by('name')
    return render(request, "auctions/categories.html",{
        "cats":cats
    })

def categories_cat(request,cat):
    return index(request,(cat,'cat'))