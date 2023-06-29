from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order  # Replace 'Order' with the actual model associated with the form
        fields =[ 'address_1','address_2']