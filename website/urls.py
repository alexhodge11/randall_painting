from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [
    path("", views.index),
    path("services/", views.services),
    path("projects/", views.projects),
    path("about/", views.about),
    path("contact/", views.contact),
    path("admin-login/", views.admin_login),
    path("dashboard/", views.dashboard),
    path("edit-projects/", views.edit_projects),
    path("edit-about-us/", views.edit_about),
    path("manage-admins/", views.manage_admins)
]