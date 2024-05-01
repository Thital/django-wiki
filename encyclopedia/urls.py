from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new_entry", views.new_entry, name="new_entry"),
    path("wiki/search", views.search, name="search"),
    path("wiki/random_page", views.random_page, name="random_page"),
    path("wiki/<str:page>", views.getpage, name="page"),
    path("wiki/<str:page>/edit", views.edit, name="edit"),
]