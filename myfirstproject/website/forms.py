from django import forms

from .models import CustomUser
from phonenumber_field.formfields import PhoneNumberField




class Aforms(forms.ModelForm):
    phone_number = PhoneNumberField()
    class Meta:
        model = CustomUser
        fields = ['email','name','phone_number', 'password']
        widgets = {
            
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'name': forms.TextInput(attrs={'class':"form-control"}),
            'password': forms.PasswordInput(render_value=True, attrs={'class': "form-control"}),
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        }

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password','phone_number']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            
        }    
        
class PriceFilterForm(forms.Form):
    min_price = forms.DecimalField(decimal_places=2)
    max_price = forms.DecimalField(decimal_places=2)   
    

  
    
    
         


