from django.db import models
from website.models import *
from store.models import *

class Payment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
   

    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')
       )

    user    = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL , blank=True, null= True) 
    order_number = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50, blank=True)  
    order_total = models.FloatField( )
    is_ordered = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


   
    
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True, null=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField( )
    price = models.FloatField( )
    ordered = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    
    
    def _str_(self):
        return f"{self.product} - {self.quantity}"

    def get_total_price(self):
        return self.quantity * self.price
