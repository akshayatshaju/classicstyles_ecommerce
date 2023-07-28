from django import forms
# from . models import Amodel
from website . models import CustomUser
from store.models import product,Category,ProductVariant,Coupon

class Aforms(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields=['email','password']
        widgets={

            'email':forms.EmailInput(attrs={'class':'form-control'}),
            #'name':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(render_value=True,attrs={'class':'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']        

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ["product_name", "category", "discription", "price","quantity","image","is_available"]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            #'Brand': forms.Select(attrs={'class': 'form-control mb-3'}),
            ' category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'discription': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            # 'image': forms.ClearableFileInput(attrs={'multiple': True}),
            
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }
                

class VariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product_name', 'color', 'size','price','stock']  
        
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'is_expired', 'discount_price', 'minimum_amount']
        widgets = {
            'coupon_code': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'is_expired': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'minimum_amount': forms.DateInput(attrs={'class': 'form-control datepicker mb-3'}),
            
        }              


