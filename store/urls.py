from django.urls import  path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('category/<slug:slug>', views.categoryproducts, name='categoryproducts'),
    path('all-products', views.allProducts, name='all-products'),
    path('product/<slug:slug>', views.productDetail, name='product-detail'),
    
    path('add-to-cart-<int:pk>/', views.addtocart, name= 'addtocart'),
    path('cart', views.cart, name='cart'),
    path('managecart<int:p_id>', views.managecart, name='managecart'),
    path('emptycart', views.emptycart, name='emptycart'),
    
    path('checkout', views.checkout, name='checkout'),

    path('register', views.registerpage, name='registerpage'),
    path('login', views.loginpage, name='loginpage'),
    path('logout', views.logoutpage, name='logoutpage'),
    path('profile', views.profile, name='profile'),
    
    path('orders', views.orders, name= 'orders'),
    path('order-detail/<int:pk>',views.orderdetail, name='orderdetail'),

    path('adminprofile', views.adminprofile, name='adminprofile'),
    path('adminpage', views.adminpage, name='adminpage'),
    path('adminpageallorders', views.adminpageallorders, name='adminpageallorders'),
    path('adminpagependingorders', views.adminpagependingorders, name='adminpagependingorders'),
    path('adminpageorderdetails/<int:pk>', views.adminpageorderdetails, name='adminpageorderdetails'),
    path('adminpageorderdetails<int:pk>/change', views.adminpageorderdetailschange, name='adminpageorderdetailschange'),
    path('adminpageallproducts', views.adminpageallproducts, name='adminpageallproducts'),
    path('adminpageaddproduct', views.adminpageaddproduct, name='adminpageaddproduct'),
    path('adminpageaddcategory', views.adminpageaddcategory, name='adminpageaddcategory'),
    path('adminpageupdateproduct/<slug:slug>', views.adminpageupdateproduct, name='adminpageupdateproduct'),
    path('adminpageallcustomers', views.adminpageallcustomers, name='adminpageallcustomers'),
    path('adminpagecontactus', views.adminpagecontactus, name='adminpagecontactus'),
    path('adminpagepromotionalemails', views.promotional_emails, name='adminpagepromotionalemails'),

    path('search', views.search, name='search'),

    path('about', views.about, name='about'),
    path('contactus', views.contactus, name='contactus'),
    
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name= 'password_change.html'), name='password_change'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name= 'reset_password.html'), name="reset_password"),
    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name= 'reset_password_sent.html'), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= 'reset_password_form.html'), name="password_reset_confirm"),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name= 'reset_password_complete.html'), name="password_reset_complete"),
]
