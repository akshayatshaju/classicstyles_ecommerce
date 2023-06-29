
from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('signout/',views.signout,name='signout'),
    path('shop/',views.shop,name='shop'),
    
    path('single_details/<int:id>/', views.single_details,name="single_details"),
    

    path('verify_code/',views.verify_code,name='verify_code'),
    path('phone_verify/',views.phone_verify,name='phone_verify'),

    
   


     
   
   
]
