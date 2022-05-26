from django.contrib import admin
from django.urls import path, include 
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index),
    path("services/", views.services),
    path("projects/", views.projects),
    path("about/", views.about),
    path("contact/", views.contact),
    path("admin-login/", views.admin_login),
    path("dashboard/", views.dashboard),
    path("manage-projects/", views.manage_projects),
    path("edit-project/<id>", views.edit_project),
    path("edit-about-us/", views.edit_about),
    path("manage-admins/", views.manage_admins),
    path("customer-hub/", views.customer_hub),
    path("update-about/", views.update_about),
    path("edit-contact/", views.edit_contact),
    path("edit-services/", views.edit_services),
    path("add-customer/", views.add_customer),
    path("delete-customer/<id>", views.delete_customer),
    path("edit-customer/<id>", views.edit_customer),
    path("update-customer/<id>", views.update_customer),
    path("add-project/", views.add_project),
    path("update-project/<id>", views.update_project),
    path("delete-project/<id>", views.delete_project),
    path("add-admin/", views.add_admin),
    path("manage-admin/", views.manage_single_admin),
    path("manage-single-admin/<id>", views.manage_single_admin),
    path("update-admin/<id>", views.update_admin),
    path("delete-admin/<id>", views.delete_admin),
    path("login/", views.login),
    path("logout/", views.logout),
    path("create-invoice/<id>", views.new_invoice)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)