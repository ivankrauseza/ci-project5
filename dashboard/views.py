from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from shop.models import Product
from shop.forms import ProductCreateForm, ProductUpdateForm
from django.urls import reverse
from django.http import HttpResponseBadRequest


# Dashboard index :
def DashboardIndex(request):
    return render(request, 'db_index.html')


# Dashboard products :
def DashboardProduct(request):
    # Products from Shop > Product model -
    products = Product.objects.all()

    # Create new product by SKU -
    if request.method == 'POST':
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            sku = form.cleaned_data['sku']
            # Check if a product with the same SKU already exists
            if Product.objects.filter(sku=sku).exists():
                return HttpResponseBadRequest("Product with this SKU already exists.")
            
            product = form.save()
            return redirect('db_product_edit', sku=product.sku)
    else:
        form = ProductCreateForm()

    # Disctionary of data
    context = {
        'products': products,
        'form': form,
    }

    return render(request, 'db_products.html', context)


# Dashboard products :
def DashboardProductCreate(request):
    return render(request, 'db_product_create.html')


# Dashboard products edit :
class DashboardProductEdit(View):
    template_name = 'db_product_edit.html'

    def get(self, request, sku):
        product = get_object_or_404(Product, sku=sku)
        form = ProductUpdateForm(instance=product)
        return render(request, self.template_name, {'form': form, 'product': product})

    def post(self, request, sku):
        product = get_object_or_404(Product, sku=sku)
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('db_product_edit', sku=product.sku)
        return render(request, self.template_name, {'form': form, 'product': product})


# Dashboard products :
def DashboardProductDelete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('db_products')

    return render(request, 'db_product_delete.html')


# Dashboard orders :
def DashboardOrder(request):
    return render(request, 'db_orders.html')
