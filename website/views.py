from random import random
from django.forms import model_to_dict, modelformset_factory
from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse
from .models import About, Customer, Admin, Project, Invoice
from django.core.exceptions import ObjectDoesNotExist
import hashlib, string, random

pepper = "asd3435fowiDu#$%^r890u2934hjDAS$#%^DF324erDylandabest"

def index(request):
    return redirect("/services/")

def services(request):
    return render(request, "services.html", context = None)

def projects(request):
    return render(request, "projects.html", context = None)

def contact(request):
    return render(request, "contact.html", context = None)

def edit_contact(request):
    if not check_session(request):
        return redirect("/services/")
    return render(request, "edit_contact_us.html", context = None)

def edit_services(request):
    if not check_session(request):
        return redirect("/services/")
    return render(request, "edit_services.html", context = None)


# About Controller

def about(request):
    context = {
        "about": About.objects.first()
    }
    return render(request, "about.html", context)

def edit_about(request):
    if not check_session(request, False):
        return redirect("/services/")
    context = {
        "about": About.objects.first()
    }
    return render(request, "edit_about_us.html", context)

def update_about(request):
    if not check_session(request, False):
        return redirect("/services/")
    about_data = About.objects.get(id = 1)
    print(f"REQUEST == {request}")
    if request.FILES:
        about_data.profile_pic = request.FILES["profile_pic"]
    about_data.profile_description = request.POST["profile_description"]
    about_data.motto = request.POST["motto"]
    about_data.co_description_header = request.POST["co_description_header"]
    about_data.co_description = request.POST["co_description"]
    about_data.save()
    return redirect("/edit-about-us/")


# Customer Hub Controller

def customer_hub(request):
    if not check_session(request, False):
        return redirect("/services/")
    context = {
        "customers": Customer.objects.all()
    }
    return render(request, "customer_hub.html", context)

def add_customer(request):
    if not check_session(request, False):
        return redirect("/services/")
    Customer.objects.create(
        first_name = request.POST["first_name"],
        last_name = request.POST["last_name"],
        phone = request.POST["phone"],
        email = request.POST["email"],
        business_name = request.POST["business_name"],
        address = request.POST["address"],
        city = request.POST["city"],
        state = request.POST["state"],
        zip_code = request.POST["zip_code"]
    )
    return redirect("/customer-hub/")

def delete_customer(request, id):
    if not check_session(request, False):
        return redirect("/services/")
    customer = Customer.objects.get(id = id)
    customer.delete()
    return redirect("/customer-hub/")

def edit_customer(request, id):
    if not check_session(request, False):
        return redirect("/services/")
    context = {
        "customer": Customer.objects.get(id = id)
    }
    return render(request, "edit_customer.html", context)

def update_customer(request, id):
    if not check_session(request, False):
        return redirect("/services/")
    customer_data = Customer.objects.get(id = id)
    customer_data.first_name = request.POST["first_name"]
    customer_data.last_name = request.POST["last_name"]
    customer_data.phone = request.POST["phone"]
    customer_data.email = request.POST["email"]
    customer_data.email = request.POST["business_name"]
    customer_data.address = request.POST["address"]
    customer_data.city = request.POST["city"]
    customer_data.state = request.POST["state"]
    customer_data.zip_code = request.POST["zip_code"]
    customer_data.save()
    return redirect("/customer-hub/")

def new_invoice(request, id):
    if not check_session(request, False):
        return redirect("/services/")
    context = {
        "customer": Customer.objects.get(id = id)
    }
    return render(request, "create_invoice.html", context) 
    

# Projects Controller

def projects(request):
    context = {
        "projects": Project.objects.all()
    }
    return render(request, "projects.html", context)

def manage_projects(request):
    if not check_session(request, False):
        return redirect("/services/")
    context = {
        "projects": Project.objects.all()
    }
    return render(request, "manage_projects.html", context)

def edit_project(request, id):
    if not check_session(request, False):
        return redirect("/services/")
    context = {
        "project": Project.objects.get(id = id)
    }
    return render(request, "edit_project.html", context)

def add_project(request):
    if not check_session(request, False):
        return redirect("/services/")
    Project.objects.create(
        photo = request.FILES["photo"],
        description = request.POST["description"],
        hidden = request.POST["hidden"]
    )
    return redirect("/manage-projects/")

def update_project(request, id):
    if not check_session(request, False):
        return redirect("/services/")
    project_data = Project.objects.get(id = id)
    project_data.description = request.POST["description"]
    project_data.hidden = request.POST["hidden"]
    project_data.save()
    return redirect("/manage-projects/")

def delete_project(request, id):
    if not check_session(request, False):
        return redirect("/services/")
    project = Project.objects.get(id = id)
    project.delete()
    return redirect("/manage-projects/")


# Admin Controller

def admin_login(request):
    return render(request, "admin_login.html", context = None)

def dashboard(request):
    if not check_session(request, False):
        return redirect("/services/")
    return render(request, "admin_dashboard.html", context = None)

def login(request):
    login_id = request.POST["user_id"]
    login_password = request.POST["password"]
    try:
        admin = Admin.objects.get(user_id = login_id)
    except ObjectDoesNotExist:
        return redirect("/admin-login/")
    print(f"PRINTING PASSWORDS: {admin.password} --> {encrypt_pass(login_password, admin.salt)}")
    x = encrypt_pass(login_password, admin.salt)
    if admin and admin.password == x[0]:
        request.session["user"] = admin.user_id
        request.session["exec_control"] = admin.exec_control
        return render(request, "admin_dashboard.html", context = None)      
    return redirect("/admin-login/")

def manage_admins(request):
    if not check_session(request, True):
        return redirect("/dashboard/")
    context = {
        "admins": Admin.objects.all()
    }
    return render(request, "manage_admins.html", context)

def add_admin(request):
    if not check_session(request, True):
        return redirect("/dashboard/")
    x = encrypt_pass(request.POST["password"])
    Admin.objects.create(
        user_id = request.POST["user_id"],
        password = x[0],
        salt = x[1],
        exec_control = request.POST["exec_control"]
    )
    return redirect("/manage-admins/")

def manage_single_admin(request, id):
    if not check_session(request, True):
        return redirect("/dashboard/")
    context = {
        "admin": Admin.objects.get(id = id)
    }
    return render(request, "manage_single_admin.html", context)

def update_admin(request, id):
    if not check_session(request, True):
        return redirect("/services/")
    admin_data = Admin.objects.get(id = id)
    admin_data.user_id = request.POST["user_id"]
    x = encrypt_pass(request.POST["password"])
    admin_data.password = x[0]
    admin_data.salt = x[1]
    admin_data.save()
    return redirect("/manage-admins/")

def delete_admin(request, id):
    if not check_session(request, True):
        return redirect("/services/")
    admin = Admin.objects.get(id = id)
    admin.delete()
    return redirect("/manage-admins/")

def logout(request):
    if not check_session(request, False):
        return redirect("/services/")
    del request.session["user"]
    del request.session["exec_control"]
    return redirect("/services/")


# Helpers

def check_session(request, needs_exec):
    if not needs_exec:
        return bool(request.session.get("user"))
    else:
        return bool(request.session.get("exec_control"))

def encrypt_pass(password, salt = None):
    if not salt:
        salt = gen_salt()
    to_encrypt = password + salt + pepper
    return hashlib.sha512(to_encrypt.encode()).hexdigest(), salt

def gen_salt():
    return "".join(random.choices(string.ascii_letters + string.digits, k = 20))