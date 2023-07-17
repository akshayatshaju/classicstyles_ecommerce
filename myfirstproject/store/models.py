from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField
from django.urls import reverse
from website.models import *


    
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique = True)
    slug = AutoSlugField(populate_from='category_name',unique=True,null=True,default=None)
    description = models.TextField(max_length=255)
    
    def get_url(self):
        return reverse('products_by_category',args= [self.slug])

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

   

    def __str__(self):
        return self.category_name
    
class product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = AutoSlugField(populate_from='product_name',unique=True,null=True,default=None)
    discription  = models.TextField(max_length=500,blank=True)
    price        = models.IntegerField()
    image        = models.ImageField(upload_to='photos/products',null=True)
    is_available  =models.BooleanField(default=True)
    category      =models.ForeignKey(Category,on_delete=models.CASCADE)
    quantity      =models.IntegerField(default=0)

    def __str__(self):
        return self.product_name
    

class ProductVariant(models.Model):
    color = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='color',unique=True,null=True,default=None)
    size = models.IntegerField()
    stock = models.IntegerField()
    product_name = models.ForeignKey(product,on_delete=models.CASCADE,related_name="product_variant")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)    


    def __str__(self):
        return self.color
    
class ProductImage(models.Model):
     product = models.ForeignKey(product, on_delete=models.CASCADE)
     image = models.ImageField(upload_to='photos/products')

     def __str__(self):
        return self.image.url
     
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

    
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)    

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    
class Coupon(models.Model): 
    coupon_code = models.CharField(max_length = 10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default = 100)
    minimum_amount = models.IntegerField(default=500)      
    
    

    

   
    

    
