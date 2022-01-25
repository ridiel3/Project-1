from django.urls import path

from encyclopedia.util import get_entry

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.search, name="search"),
    path("wiki/random", views.random_page, name="random"),
    path("wiki/new", views.new_entry, name="new"),
    path("wiki/add", views.add_entry, name="add"),
    path("wiki/edit_page", views.save_edited_entry, name="save"),
    path("wiki/<str:title>", views.pages, name="pages"),
    path("edit/<str:title>", views.edit_entry, name="edit")
]
