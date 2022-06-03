import email
import os
from random import random
from tkinter import Canvas
from tkinter.filedialog import SaveAs
from unicodedata import name
from django.forms import model_to_dict, modelformset_factory
from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages

from randall_painting.settings import MEDIA_URL
from .models import About, Customer, Admin, Project, Invoice
from django.core.exceptions import ObjectDoesNotExist
import hashlib, string, random
from django.core.mail import send_mail
from datetime import date, datetime

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from randall_painting.settings import MEDIA_ROOT

from django.core.files.storage import default_storage

pepper = "asd3435fowiDu#$%^r890u2934hjDAS$#%^DF324erDylandabest"

def index(request):
    return redirect("/services/")

def services(request):
    return render(request, "services.html", context = None)

def projects(request):
    return render(request, "projects.html", context = None)

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

def customer_invoices(request, id):
    if not check_session(request, False):
        return redirect("/services/")
    context = {
        "invoices": Invoice.objects.filter(invoice_id = id),
        "customer": Customer.objects.get(id = id)
    }
    print(context["invoices"])
    return render(request, "customer_invoices.html", context)

def generate_invoice(request, id):
    if not check_session(request, False):
        return redirect("/services/")

    #reportlab
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    phone = request.POST["phone"]
    email = request.POST["email"]
    business_name = request.POST["business_name"]
    address = request.POST["address"]
    city = request.POST["city"]
    state = request.POST["state"]
    zip_code = request.POST["zip_code"]
    labor_cost = request.POST["labor_cost"]
    supplies_cost = request.POST["supplies_cost"]

    generated_invoice = generate_label(last_name, business_name)

    tax = (float(labor_cost) + float(supplies_cost)) * 0.27

    subtotal = (float(labor_cost) + float(supplies_cost)) 

    grand_total = float(labor_cost) + float(supplies_cost) + tax

    labor_cost = "{:.2f}".format(float(labor_cost))
    supplies_cost = "{:.2f}".format(float(supplies_cost))
    subtotal = "{:.2f}".format(subtotal)
    tax = "{:.2f}".format(tax)
    grand_total = "{:.2f}".format(grand_total)

    save_name = os.path.join(MEDIA_ROOT, 'invoices_folder', f"{generated_invoice}.pdf")

    print(save_name)

    # buffer = io.BytesIO()
    c = canvas.Canvas(save_name, pagesize=letter, bottomup=0) 
    #buffer
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    lines = [
        f"INVOICE ID: ",
        f"     {generated_invoice}",
        " ",
        " ",
        f"NAME:    {first_name} {last_name}",
        " ",
        f"PHONE:    {phone}",
        " ",
        f"EMAIL:    {email}",
        " ",
        f"BUSINESS NAME:    {business_name}",
        f"ADDRESS:",
        f"   {address}",
        f"   {city}, {state}   {zip_code}",
        " ",
        " ",
        " ",
        f"LABOR:    ${str(labor_cost)}",
        f"SUPPLIES:    ${str(supplies_cost)}",
        " ",
        f"SUBTOTAL: ${subtotal}",
        f"TAX:    ${str(tax)}",
        " ",
        f"GRAND TOTAL:    ${str(grand_total)}"
    ]

    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()

    Invoice.objects.create(
        invoice = Customer.objects.get(id = request.POST["customer_id"]),
        invoice_location = f"/media/invoices_folder/{generated_invoice}.pdf",
        invoice_label = generated_invoice
    )

    # context = {
    #     "customer": Customer.objects.get(id = id)
    # }

    return redirect(f"/customer-invoices/{id}")

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
    print(f"PHOTO: {type(request.FILES['photo'])}")
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

def login_user(request):

    errors = Admin.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect("/admin-login/")

    else:
        login_id = request.POST["user_id"]
        login_password = request.POST["password"]
        try:
            admin = Admin.objects.get(user_id = login_id)
        except ObjectDoesNotExist:
            return redirect("/admin-login/")
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


#Contact Controller

def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]
        message = request.POST["message"]

        #subject, message, from email, to email
        send_mail(
            f"Business Inquiry - {name}",
            f"""
MESSAGE:  {message}

PHONE NUMBER:  {phone_number}

EMAIL:  {email}

""",
            email,
            ["aahodge11@gmail.com"]
        )
        return render(request, "success.html", context = None)
    else:
        return render(request, "contact.html", context = None)

def process_contact(request):
    pass

def contact_success(request):
    return render(request, "success.html", context = None)


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

def generate_label(lname, bname):
    now = datetime.now()

    month = now.strftime("%m")
    day = now.strftime("%d")
    year = now.strftime("%Y")
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    second = now.strftime("%S")

    return (f"{year}_{month}_{day}_{lname.lower()}_business_name_{bname.lower()}_{hour}_{minute}_{second}").replace(" ", "_")