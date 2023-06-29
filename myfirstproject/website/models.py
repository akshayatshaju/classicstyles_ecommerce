

# Create your models here.

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
#from.models import Website
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, name, phone_number, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name,  phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name,  phone_number, password, **extra_fields)

    def create_superuser(self, email, name, phone_number, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100,null=True)
    phone_number= PhoneNumberField(null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone_number']

    objects = CustomUserManager()

#Address
class AddressBook(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="addresses")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10,null=True)
    status = models.BooleanField(default=False)    


    def __str__(self):
        return str(self.user)     

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique = True)
    slug = AutoSlugField(populate_from='category_name',unique=True,null=True,default=None)
    description = models.TextField(max_length=255)
    

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
