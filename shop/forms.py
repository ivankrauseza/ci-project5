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