from django.contrib import admin
from .models import *



# Register your models here.
admin.site.register(Category)
admin.site.register(product)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)

admin.site.register(Wishlist)
admin.site.register(Coupon)

