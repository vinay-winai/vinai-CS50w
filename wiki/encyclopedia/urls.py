from django.urls import path

from . import views

# app_name = "encylopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("new", views.new, name="new"),
]
