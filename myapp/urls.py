"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home-02/', views.home2, name='home-02'),
    path('home-03/', views.home3, name='home-03'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('product/', views.product, name='product'),
    path('product-detail/<int:pk>/', views.pdetail, name='product-detail'),
    path('shopingcart/', views.shopingcart, name='shopingcart'),
    path('contact/', views.contact, name='contact'),
    path('blogdetail/', views.blogdetail, name='blogdetail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('verifyotp/', views.verifyotp, name='verifyotp'),
    path('newpass/', views.newpass, name='newpass'),
    path('changepass/', views.changepass, name='changepass'),
    path('profileupdate/', views.profileupdate, name='profileupdate'),
    path('sindex/', views.sindex, name ='sindex'),
    path('spass/', views.changepass, name='spass'),
    path('sprofile/', views.profileupdate, name='sprofile'),
    path('sadd/', views.sadd, name='sadd'),
    path('sview/', views.sview, name='sview'),
    path('sedit/<int:pk>/', views.sedit, name='sedit'),
    path('sdelete/<int:pk>/', views.sdelete, name='sdelete'),
    path('buyer-product-detail/<int:pk>/',views.buyer_product_detail,name='buyer-product-detail'),
    path('add-to-wishlist/<int:pk>/',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove-from-wishlist/<int:pk>/',views.remove_from_wishlist,name='remove-from-wishlist'),
    path('add-to-cart/<int:pk>/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart,name='cart'),
    path('remove-from-cart/<int:pk>/',views.remove_from_cart,name='remove-from-cart'),
    path('change-qty/<int:pk>/',views.change_qty,name='change-qty'),
    path('create-checkout-session/', views.create_checkout_session, name='payment'),
    path('success.html/', views.success,name='success'),
    path('cancel.html/', views.cancel,name='cancel'),
    path('ajax/validate_email/',views.validate_signup,name='validate_email'),
]