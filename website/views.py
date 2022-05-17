from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse

def index(request):
    return redirect("/services/")

def services(request):
    return render(request, "services.html", context = None)

def projects(request):
    return render(request, "projects.html", context = None)

def about(request):
    return render(request, "about.html", context = None)

def contact(request):
    return render(request, "contact.html", context = None)

def admin_login(request):
    return render(request, "admin_login.html", context = None)

def dashboard(request):
    return render(request, "admin_dashboard.html", context = None)

def edit_projects(request):
    return render(request, "edit_projects.html", context = None)

def edit_about(request):
    return render(request, "edit_about_us.html", context = None)

def manage_admins(request):
    return render(request, "manage_admins.html", context = None)