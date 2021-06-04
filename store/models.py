from enum import auto
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

class Customer(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    phone= PhoneNumberField(null=True)
    email= models.EmailField(null=True)
    image= models.ImageField(upload_to= 'customers_images', default='profile2.png')
    promo_emails= models.BooleanField(default=True)
    joined_on= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    title= models.CharField(max_length=255)
    slug= models.SlugField(unique=True)

    class Meta:
        verbose_name_plural= 'categories'

    def __str__(self):
        return self.title

class Product(models.Model):
    title= models.CharField(max_length=255)
    slug= models.SlugField(unique=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    image= models.ImageField(upload_to='products')
    marked_price= models.PositiveIntegerField()
    selling_price= models.PositiveIntegerField()
    description= models.TextField()
    warranty= models.CharField(max_length=1000, null=True, blank=True)    
    return_policy= models.CharField(max_length=1000, null=True, blank=True)    

    def __str__(self):
        return self.title
    
class Cart(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total= models.PositiveIntegerField(default=0)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Cart:' + str(self.id)

class CartProduct(models.Model):
    cart= models.ForeignKey(Cart, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    rate= models.PositiveIntegerField()
    quantity= models.PositiveIntegerField()
    subtotal= models.PositiveIntegerField()

    def __str__(self):
        return 'Cart:' + str(self.cart.id) + 'Cart Product:' + str(self.id)
    
ORDER_STATUS= (
        ('Order Received', 'Order Received'),
        ('Order Processing', 'Order Processing'),
        ('On The Way', 'On The Way'),
        ('Order Completed', 'Order Completed'),
        ('Order Cancelled', 'Order Cancelled'),
    )
    

class Order(models.Model):
    
    cart= models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by= models.CharField(max_length=255)
    mobile= models.CharField(max_length=15)
    email= models.EmailField()
    shipping_address= models.CharField(max_length=500)
    city= models.CharField(max_length=200)
    state= models.CharField(max_length=200)
    pincode= models.IntegerField()
    subtotal= models.PositiveIntegerField()
    discount= models.PositiveIntegerField()
    total= models.PositiveIntegerField()
    order_status= models.CharField(max_length=255, choices=ORDER_STATUS)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Order:' + str(self.id)
    
class ContactUs(models.Model):
    name= models.CharField(max_length=255)
    email= models.EmailField()
    phone= PhoneNumberField()
    query= models.TextField()
    date_submitted= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural= 'contact us'
    