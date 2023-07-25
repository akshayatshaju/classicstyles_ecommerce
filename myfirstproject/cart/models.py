from django.db import models
from website.models import *
from store.models import *



<<<<<<< HEAD
# cart
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ProductVariant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


""" 
=======
    
>>>>>>> 26be664ff2e5f3571244736f4949380e03955267
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_id = models.AutoField(primary_key=True)
    razor_pay_order_id = models.CharField(max_length =100, null =True, blank=True)
    razor_pay_payment_id = models.CharField(max_length =100, null =True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length =100, null =True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True,blank=True)
    



    def get_total_price(self):
        return sum(item.sub_total() for item in self.cart_items.all())
<<<<<<< HEAD
=======
        
>>>>>>> 26be664ff2e5f3571244736f4949380e03955267
    
    # def get_total_products(self):
    #     return sum(item.quantity for item in self.Cart_Item.all())




class Cart_Item(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    carts = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cart_items')  

    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

    class Meta:
        managed = True
    
    
    def sub_total(self):
        return self.product_variant.price * self.quantity 
    
        
    
"""   