from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,ListingForm


def index(request):
    return render(request, "auctions/index.html")


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
    """New user registration page."""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation and not field is left blank.
        password = request.POST["password"]
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
    

@login_required
def new_listing(request):
    if request.method == "POST":
        my_querydict = request.POST.copy()
        my_querydict['user'] = request.user
        form = ListingForm(my_querydict)
        if form.is_valid():
            title = form.cleaned_data['title']
            form.save()
            return  HttpResponseRedirect(reverse('index',))
        return render(request, "auctions/newlisting.html", {
                "message" : "Illegal entry.",
                "form": form,
            })
    return render(request, "auctions/newlisting.html",{
                "form": ListingForm,
        })


def listing(request):
    pass

@login_required
def watch_list(request):
    pass

def categories(request):
    pass
