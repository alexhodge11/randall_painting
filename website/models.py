from distutils.command.upload import upload
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone
from django.db.models.functions import Now
import datetime
from random import random
import hashlib, string, random
from django.core.exceptions import ObjectDoesNotExist

pepper = "asd3435fowiDu#$%^r890u2934hjDAS$#%^DF324erDylandabest"

# Create your models here.

class Customer(models.Model):
    first_name = models.TextField(max_length = 25)
    last_name = models.TextField(max_length = 25)
    phone = models.IntegerField()
    email = models.TextField(max_length = 50)
    business_name = models.TextField(blank=True)
    address = models.TextField()
    city = models.TextField(max_length = 30)
    state = models.TextField(max_length = 2)
    zip_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Invoice(models.Model):
    invoice = models.ForeignKey(Customer, related_name = "invoices", on_delete = models.CASCADE)
    invoice_location = models.FileField(upload_to = "invoices_folder", blank = True)
    invoice_label = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class AdminManager(models.Manager):
    def basic_validator(self, postData):
        print(postData)
        login_admin = postData["user_id"]
        errors = {}
        try:
            admin = Admin.objects.get(user_id = postData["user_id"])
        except ObjectDoesNotExist:
            errors["user_id"] = "Incorrect username or password"
            return errors

        password = postData["password"]

        salt = admin.salt
        x = encrypt_pass(password, salt)
        enc_password = x[0]

        if admin.user_id == login_admin and admin.password == enc_password:    
            return errors
        else:
            errors["password"] = "Incorrect username or password"
        return errors

class Admin(models.Model):
    user_id = models.TextField(max_length = 20)
    salt = models.TextField(blank = True)
    password = models.TextField()
    exec_control = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AdminManager()

class Project(models.Model):
    photo = models.ImageField(upload_to = "projects", blank = True)
    description = models.TextField()
    hidden = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class About(models.Model):
    motto = models.TextField()
    profile_pic = models.ImageField(upload_to = "profile_pic", blank = True)
    profile_description = models.TextField()
    co_description_header = models.TextField()
    co_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def encrypt_pass(password, salt = None):
    if not salt:
        salt = gen_salt()
    to_encrypt = password + salt + pepper
    return hashlib.sha512(to_encrypt.encode()).hexdigest(), salt

def gen_salt():
    return "".join(random.choices(string.ascii_letters + string.digits, k = 20))