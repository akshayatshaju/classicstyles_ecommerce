
from django.urls import path
from . import views

urlpatterns = [
  path('admin_panel', views.admin_panel,name="admin_panel"),
  path('admin_login', views.admin_login,name="admin_login"),
  path('admin_logout', views.admin_logout,name="admin_logout"),

  path('user', views.user,name="user"),
  path('block_user/<int:id>/', views.block_user,name="block_user"),
  path('unblock_user/<int:id>/', views.unblock_user,name="unblock_user"),
  
 
  path('add_product/',views.add_product,name="add_product"),
  path('edit_product/<int:id>/',views.edit_product,name="edit_product"),
  path('del_product/<int:id>/',views.del_product,name="del_product"),

  path('category_list/',views.category_list,name="category_list"),
  path('del_category/<int:id>/',views.del_category,name="del_category"),
  path('edit_category/<int:id>/',views.edit_category,name="edit_category"),
  path('add_category/',views.add_category,name="add_category"),
  

  path('product_variant', views.product_variant,name="product_variant"),
  path('del_product_variant/<int:id>/', views.del_product_variant,name="del_product_variant"),
  path('edit_product_variant/<int:id>/', views.edit_product_variant,name="edit_product_variant"),
  path('add_product_variant', views.add_product_variant,name="add_product_variant"),
  
  path('orders', views.orders,name="orders"),
  path('edit_order/<int:id>/', views.edit_order,name="edit_order"),
  path('order_products/<int:id>/', views.order_products,name="order_products"),
  
  
  
  path('Product_list/',views.Product_list,name="Product_list"),
  
  
  path('coupen_manage/',views.coupen_manage,name="coupen_manage"),
  path('add_coupons/',views.add_coupons,name="add_coupons"),
  path('del_coupons/<int:id>/',views.del_coupons,name="del_coupons"),
  path('edit_coupons/<int:id>/',views.edit_coupons,name="edit_coupons"),
  
  path('dashboard',views.dashboard,name="dashboard"),
  
  
  
  
  
  ]