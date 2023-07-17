
from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('signout/',views.signout,name='signout'),
    
    
    path('single_details/<int:id>/', views.single_details,name="single_details"),
    

    path('verify_code/',views.verify_code,name='verify_code'),
    path('phone_verify/',views.phone_verify,name='phone_verify'),
    
    
    path('shop/',views.shop,name='shop'),
    path('shop/<slug:category_slug>/', views.shop, name='products_by_category'),
    
    path('search_brand/',views.search_brand,name='search_brand'),
    
    
    path('orderlist/',views.orderlist,name='orderlist'),
    
    
    path('create_user_profile/',views.create_user_profile,name='create_user_profile'),
    
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('forgotPassword_otp/',views.forgotPassword_otp,name='forgotPassword_otp'),
    path('resetPassword/',views.resetPassword,name='resetPassword'),
    
    path('price_filter/',views.price_filter,name='price_filter'),
    
    
    
    
    

    
]
