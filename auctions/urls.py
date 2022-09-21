from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.new_listing, name="newlisting"),
    path("listing", views.listing, name="listing"),
    path("watchlist", views.watch_list, name="watchlist"),
    path("categories", views.categories, name="categories"),
]
