from django.db import models
from website.models import *
from store.models import *

class Payment(models.Model):
    payment_choices=(
        ('COD','COD'),
        
        ('Razorpay','Razorpay'),
        
    )

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100,null=True)
    payment_method = models.CharField(max_length=100,choices=payment_choices)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
   
    def __str__(self):
        return f"{self.user.name}--{self.payment_method}"
    
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
    status = models.CharField(max_length=50,choices=STATUS,default='New')
    cancellation_reason = models.TextField(blank=True)
    return_reason = models.TextField(blank=True)
    


   
    
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="myorders")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True, null=True)
    ProductVariant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField( )
    price = models.FloatField( )
    ordered = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    
    
    def _str_(self):
        return f"{self.ProductVariant} - {self.quantity}"

    def get_total_price(self):
        return self.quantity * self.price
    
class CancelOrder(models.Model):
    reasons = {
        ('Wrong Size','Wrong Size'),
        ('Other reasons','Other reasons'),

    }
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    cancel_reason = models.CharField(max_length=100,choices=reasons)      
    
    
class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   

    def str(self):
        return f"Wallet for {self.user.username}"      
