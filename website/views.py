from django.http import HttpRequest
from django.shortcuts import render, HttpResponse

def services(request):
    return render(request, "services.html", context = None)

def projects(request):
    return render(request, "projects.html", context = None)

def about(request):
    return render(request, "about.html", context = None)

def contact(request):
    return render(request, "contact.html", context = None)