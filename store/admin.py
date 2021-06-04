from django.contrib import admin
from .models import *

admin.site.register([Cart, CartProduct, Order, ContactUs])

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display= ['name', 'phone', 'email', 'image', 'promo_emails']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('title',)}
    list_filter= ['category']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('title',)}


