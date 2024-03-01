from django import forms
from .models import CustomerDeliveryAddress


class CustomerDeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerDeliveryAddress
        fields = ['street', 'city', 'state', 'postal_code', 'country']