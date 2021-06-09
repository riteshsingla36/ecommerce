from django import forms
from django.db import models
from django.db.models import fields
from django.http import request
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

class CustomerForm(ModelForm):
    class Meta:
        model= Customer
        fields= '__all__'
        exclude= ['user']

class OrderForm(forms.ModelForm):
    class Meta:
        model= Order
        fields= ['ordered_by', 'mobile', 'email','shipping_address', 'city', 'state', 'pincode', 'payment_image']

class CreateProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields= '__all__'
    
class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model= Category
        fields= '__all__'

class ContactUsForm(forms.ModelForm):
    class Meta:
        model= ContactUs
        fields= '__all__'