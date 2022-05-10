from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [
    path("services/", views.services),
    path("projects/", views.projects),
    path("about/", views.about),
    path("contact/", views.contact)
]