import django
from django.db import reset_queries
from store.models import Product
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import admin_only, unauthoriseduser
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail


def index(request):
    all_products= Product.objects.all().order_by('-id')
    carousel_products= Product.objects.all().order_by('-id')[0]
    carousel_product= Product.objects.all().order_by('-id')[1:3]
    paginator = Paginator(all_products, 8)
    page_number = request.GET.get('page')
    products_list = paginator.get_page(page_number)
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    if group == 'admin':
        return redirect('adminpage')
    
    context= {'products_list': products_list, 'carousel_products': carousel_products, 'carousel_product': carousel_product}
    return render(request, 'home.html', context)

def categoryproducts(request, slug):
    category= Category.objects.get(slug= slug)
    products_list= Product.objects.filter(category=category)
    paginator = Paginator(products_list, 8)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    context= {'category': category, 'products': products}
    return render(request, 'categoryproducts.html', context)

def allProducts(request):
    allcategories= Category.objects.all()
    context= {'allcategories': allcategories}
    return render(request, 'allproducts.html', context)

def productDetail(request, slug):
    product= Product.objects.get(slug=slug)
    context= {'product': product}
    return render(request, 'productdetail.html', context)

def addtocart(request, pk):
    # get product id
    product_id= pk

    # get product
    product_obj= Product.objects.get(id= pk)

    # check if cart already exists
    cart_id= request.session.get('cart_id', None)
    if cart_id:
        cart= Cart.objects.get(id=cart_id)
        if request.user.is_authenticated:
            cart.customer= request.user.customer
            cart.save()
        # check if product already exists in cart or not
        is_this_product_in_cart= cart.cartproduct_set.filter(product=product_obj)
        
        if is_this_product_in_cart.exists():
            cartproduct= is_this_product_in_cart.last()
            cartproduct.quantity += 1
            cartproduct.subtotal += product_obj.selling_price
            cartproduct.save()
            cart.total += product_obj.selling_price
            cart.save()
        else:
            cartproduct= CartProduct.objects.create(cart=cart, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal= product_obj.selling_price)
            cart.total+= product_obj.selling_price
            cart.save()

    else:
        cart= Cart.objects.create(total=0)
        request.session['cart_id']= cart.id
        cartproduct= CartProduct.objects.create(cart=cart, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal= product_obj.selling_price)
        cart.total+= product_obj.selling_price
        cart.save()
        
    context= {}
    return redirect('/')

def cart(request):
    cart_id= request.session.get('cart_id', None)
    if cart_id:
        cart= Cart.objects.get(id=cart_id)
    else:
        cart= None
    context= {'cart': cart}
    return render(request, 'cart.html', context)

def managecart(request, p_id):
    product_id= p_id
    action= request.GET.get('action')
    cp= CartProduct.objects.get(id= product_id)
    cart= cp.cart
    if action== "inc":
        cp.quantity += 1
        cp.subtotal += cp.rate
        cp.save()
        cart.total += cp.rate
        cart.save()
    elif action== "dec":
        cp.quantity -= 1
        cp.subtotal -= cp.rate
        cp.save()
        cart.total -= cp.rate
        cart.save()
        if cp.quantity== 0:
            cp.delete()
    elif action== 'rmv':
        cart.total -= cp.subtotal
        cart.save()
        cp.delete()
    else:
        pass
    return redirect('cart')

def emptycart(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart= Cart.objects.get(id= cart_id)
        cart.cartproduct_set.all().delete()
        cart.total= 0
        cart.save()
    return redirect('cart')

@login_required(login_url='loginpage')
def checkout(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart= Cart.objects.get(id= cart_id)
        if request.user.is_authenticated:
            cart.customer= request.user.customer
            cart.save()
        form= OrderForm()
        if request.method== 'POST':
            form= OrderForm(request.POST)
            form.instance.cart= cart
            form.instance.subtotal= cart.total
            form.instance.discount= 0
            form.instance.total= cart.total-form.instance.discount
            form.instance.order_status= 'Order Received'
            if form.is_valid():
                form.save()
                del request.session['cart_id']
                return redirect('home')    
    else:
        cart= None
        return redirect('home')
    
    context = {'cart': cart, 'form': form}
    return render(request, 'checkout.html', context)

@unauthoriseduser
def registerpage(request):
    if request.method== 'POST':
        username= request.POST.get('username')
        email= request.POST.get('email')
        password1= request.POST.get('password1')
        password2= request.POST.get('password2')

        values= {
            'username': username,
            'email': email
        }
        error_message= None
        
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    
        if len(username)<4 or len(username)>15:
            error_message= 'Username must be longer than 4 characters'
        
        elif not any(char.isdigit() for char in password1) or not any(char.isalpha() for char in password1) or not any(char in special_characters for char in password1):
            error_message= 'password must contain a digit, a number and a special character'

        elif password1 != password2:
            error_message= 'Password does not match'

        elif User.objects.filter(username= username):
            error_message= 'Another user with same username already exists'
            
        elif User.objects.filter(email= email):
            error_message= 'Another user with same email already exists'

        if not error_message:
            user= User.objects.create_user(
                username= username,
                email= email,
                password= password1
            )

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            customer= Customer.objects.create(
                user= user,
                name= username,
                email= email,
            )

            user.save()
            customer.save()
            send_mail(
                'Welcome To Eshop',
                'Thankyou for becoming a member of our team'
                'rsjkq9@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Account was created for '+ username)
            return redirect('loginpage')
        else:
            context= {'error_message': error_message, 'values': values}
            return render(request, 'register.html', context)
    return render(request, 'register.html')

@unauthoriseduser
def loginpage(request):
    if request.method== 'POST':
        email= request.POST.get('email')
        password= request.POST.get('password')

        try:
            usere= User.objects.get(email= email)
            username= usere.username            
        except:
            usere= None

        if usere:
            user= authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                group = None
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name

                if group == 'admin':
                    return redirect('adminpage')
                else:
                    return redirect('home')
            else:
                messages.info(request, "Email or Password is Incorrect...")
        else:
            messages.info(request, 'Email or password is incorrect...')
    return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    return redirect('loginpage')

@login_required(login_url='loginpage')
def profile(request):
    customer= request.user.customer
    form= CustomerForm(instance=customer)
    if request.method== 'POST':
        form= CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context= {'customer': customer, 'form': form}
    return render(request, 'profile.html',context)

@login_required(login_url='loginpage')
def orders(request):
    orders= Order.objects.filter(cart__customer= request.user.customer).order_by('-id')
    context= {'orders': orders}
    return render(request, 'orders.html', context)

@login_required(login_url='loginpage')
def orderdetail(request, pk):
    order= Order.objects.get(id=pk)
    if request.user.customer != order.cart.customer:
        return redirect('orders')
    context= {'order': order}
    return render(request, 'orderdetail.html', context)

@admin_only
def adminpage(request):
    total_orders= Order.objects.all().count()
    received= Order.objects.filter(order_status= 'Order Received').count()
    processing= Order.objects.filter(order_status= 'Order Processing').count()
    shipped= Order.objects.filter(order_status= 'On The Way').count()
    completed= Order.objects.filter(order_status= 'Order Completed').count()
    cancelled= Order.objects.filter(order_status= 'Order Cancelled').count()
    context= {'total_orders': total_orders, 'completed': completed, 'received': received, 'processing':processing, 'shipped': shipped, 'cancelled': cancelled}
    return render(request, 'admin/adminpage.html', context)

@admin_only
def adminpageallorders(request):
    orders= Order.objects.all().order_by('-id')
    context= {'orders': orders}
    return render(request, 'admin/adminpageallorders.html', context)

@admin_only
def adminpagependingorders(request):
    pending_orders= Order.objects.filter(order_status= 'Order Received').order_by('-id')
    context= {'pending_orders':pending_orders}
    return render(request, 'admin/adminpagependingorders.html', context)

@admin_only
def adminpageorderdetails(request, pk):
    order= Order.objects.get(id=pk)
    all_status= ORDER_STATUS
    context= {'order': order, 'all_status': all_status}
    return render(request, 'admin/adminpageorderdetails.html', context)

@admin_only
def adminpageorderdetailschange(request, pk):
    order= Order.objects.get(id=pk)
    if request.method== 'POST':
        new_status= request.POST.get('status')
        order.order_status= new_status
        order.save()
    return redirect('adminpageorderdetails', pk)

@admin_only
def adminpageallproducts(request):
    products= Product.objects.all().order_by('-id')
    context= {'products': products}
    return render(request, 'admin/adminpageallproducts.html', context)

@admin_only
def adminpageaddproduct(request):
    form= CreateProductForm()
    if request.method== "POST":
        form= CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminpageallproducts')
    context= {'form': form}
    return render(request, 'admin/adminpageaddproduct.html', context)

@admin_only
def adminpageaddcategory(request):
    form= CreateCategoryForm()
    if request.method=='POST':
        form= CreateCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpageaddcategory')
    context= {'form': form}
    return render(request, 'admin/adminpageaddcategory.html', context)

@admin_only
def adminpageupdateproduct(request, slug):
    product= Product.objects.get(slug=slug)
    form= CreateProductForm(instance=product)
    if request.method== "POST":
        form= CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('adminpageallproducts')
    context= {'form': form}
    return render(request, 'admin/adminpageupdateproduct.html', context)

@admin_only
def adminprofile(request):
    customer= request.user.customer
    form= CustomerForm(instance=customer)
    if request.method== 'POST':
        form= CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context= {'customer': customer, 'form': form}
    return render(request, 'admin/adminprofile.html', context)

@admin_only
def adminpageallcustomers(request):
    customers= Customer.objects.all()
    context= {'customers': customers}
    return render(request, 'admin/adminpageallcustomers.html', context)

@admin_only
def adminpagecontactus(request):
    queries= ContactUs.objects.all()
    context= {'queries': queries}
    return render(request, 'admin/adminpagecontactus.html', context)

@admin_only
def promotional_emails(request):
    customers = Customer.objects.filter(promo_emails= True)
    for customer in customers:
        print(customer.email)
    if request.method== 'POST':
        subject= request.POST.get('subject')
        message= request.POST.get('message')
        for customer in customers:
            send_mail(
                    subject,
                    message,
                    'your email here',
                    [customer.email],
                    fail_silently=False,
                )
        messages.success(request, 'All emails heve been sent.....')
    return render(request, 'admin/adminpagepromotionalemails.html')

def search(request):
    query= request.GET.get('search')
    results= Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    context= {'results': results}
    return render(request, 'search.html', context)

def about(request):
    return render(request, 'about.html')

def contactus(request):
    form= ContactUsForm()
    if request.method== 'POST':
        form= ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Query Submitted Successfully')
            return redirect('contactus')
    context= {'form': form}
    return render(request, 'contactus.html', context)