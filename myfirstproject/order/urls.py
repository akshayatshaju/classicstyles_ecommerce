from django.urls import path
from . import views

urlpatterns = [
      #payment
    
    
    path('confirm_order/',views.confirm_order,name="confirm_order"),
    
    path('place_order', views.place_order, name='place_order'),

    
    path('place_order_razorpay', views.place_order_razorpay, name='place_order_razorpay'),
    
    
    path('complete_payment/', views.complete_payment, name='complete_payment'),
    
    
    
]