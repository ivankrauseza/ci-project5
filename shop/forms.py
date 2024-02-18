from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku']

    # Remove any spaces from the SKU -
    def clean_sku(self):
        sku = self.cleaned_data['sku']
        cleaned_sku = sku.replace(" ", "").upper()
        return cleaned_sku

    def save(self, commit=True):
        product = super().save(commit=False)
        product.blocked = True  # Assign 'true' to the blocked field
        if commit:
            product.save()
        return product


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'blurb', 'desc', 'stock', 'price', 'category', 'brand', 'blocked', 'type']

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        # Clean SKU as needed (e.g., remove spaces and capitalize)
        cleaned_sku = sku.replace(" ", "").upper()
        return cleaned_sku


class AddToBasketForm(forms.Form):
    def __init__(self, max_quantity, *args, **kwargs):
        super(AddToBasketForm, self).__init__(*args, **kwargs)
        self.fields['quantity'] = forms.IntegerField(
            initial='1',
            label='',
            widget=forms.NumberInput(attrs={
                'min': 1,
                'input_type': 'number',
                'step': 1,
                'style': 'float:left;appearance: textfield; text-align:center',
                'class': 'form-control'
                }),
            validators=[
                MinValueValidator(limit_value=1, message='Must be at least 1'),
                MaxValueValidator(limit_value=max_quantity, message='Exceeds available stock')
            ]
        )

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        try:
            # Try to convert the input to an integer
            quantity = int(quantity)
        except ValueError:
            # If conversion fails, raise a validation error
            raise forms.ValidationError('Enter a valid number.')
        return quantity
