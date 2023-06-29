from django.db import models


# class Category(BaseModel):
#     category_name = models.CharField(max_length=255,null=True)
#     slug = models.SlugField(unique=True, null =True, blank=True)
#     category_image = models.ImageField(upload="categories")

# class Product(BaseModel):
#     product_name = models.Charfield(max_lemgth=100)
#     slug = models.SlugField(unique=True,null =True, blank=True)
#     category = models.ForeignKey(Category , on_delete=models.CASCADE, related_name="products")
#     price = models.IntegerField()
#     producr_description = models.TextField()

# class Productimage(BaseModel):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
#     image = models.ImageField(upload="product")






    # def __str__(self):
    #     if self.name==None:
    #         return "ERROR- NAME IS NULL"
    #     return self.name


# class Subcategory(models.Model):
#     name = models.CharField(max_length=255,null=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)

#     def __str__(self):
#         if self.name==None:
#             return "ERROR- NAME IS NULL"
#         return self.name


# class product(models.Model):
#     name = models.CharField(max_length=255,null=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

#     def __str__(self):
#         if self.name==None:
#             return "ERROR- NAME IS NULL"
#         return self.name
