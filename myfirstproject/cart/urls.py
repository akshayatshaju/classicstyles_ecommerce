from django.urls import path
from . import views

urlpatterns = [
    
   path('add_cart',views.add_cart,name="add_cart"),
   path('view_cart',views. view_cart,name="view_cart"),
   path('update_cart_item_quantity',views. update_cart_item_quantity,name="update_cart_item_quantity"),
   path('delete_from_cart/<int:cart_item_id>/', views.delete_from_cart, name="delete_from_cart"),
   path('chech_out/', views.chech_out.as_view(), name='chech_out'),
   path('add_address/',views.add_address,name='add_address'),
   path('edit_address/<int:id>/',views.edit_address,name='edit_address'),
   path('del_addresss/<int:id>/',views.del_address,name='del_address'),

    path('userprofile',views.userprofile,name='userprofile'),

   #payment
    path('payment_product/<int:id>/',views.payment_product,name='payment_product'),
    

    
]

