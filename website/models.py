from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone
from django.db.models.functions import Now
import datetime

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
    invoice = models.ForeignKey(Customer, related_name = "invoices", on_delete=models.CASCADE)
    invoice_label = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Admin(models.Model):
    user_id = models.TextField(max_length = 20)
    salt = models.TextField(blank = True)
    password = models.TextField()
    exec_control = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = Login()

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

class Login(models.Manager):
    def login_validation(self, postData):
        errors = {}
        if not postData["user_id"] or postData["password"]:
            errors["user_id"] = "Incorrect login or password."
        return errors