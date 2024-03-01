from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from shop.models import Product, File, Order, Transaction
from shop.forms import ProductCreateForm, ProductUpdateForm, FileForm
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
        product_form = ProductUpdateForm(instance=product)
        file_form = FileForm(request.POST, request.FILES)
        
        files = File.objects.filter(product=product)

        return render(request, self.template_name, {
            'product_form': product_form,
            'file_form': file_form,
            'product': product,
            'files': files
        })

    def post(self, request, sku):
        product = get_object_or_404(Product, sku=sku)
        product_form = ProductUpdateForm(request.POST, instance=product)
        file_form = FileForm(request.POST, request.FILES)

        if file_form.is_valid():
            file_instance = file_form.save(commit=False)
            file_instance.product = product
            file_instance.save()
            return redirect('db_product_edit', sku=product.sku)

        if product_form.is_valid():
            product_form.save()
            return redirect('db_product_edit', sku=product.sku)

        return render(request, self.template_name, {
            'product_form': product_form,
            'file_form': file_form,
            'product': product
            })


# Delete product image :
class FileDeleteView(View):
    def post(self, request, *args, **kwargs):
        file_id = kwargs.get('file_id')
        file = get_object_or_404(File, pk=file_id)
        sku = file.product.sku

        # Delete the file
        file.delete()

        # Redirect back to the product edit page
        return redirect('db_product_edit', sku=sku)


# Dashboard products :
def DashboardProductDelete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('db_products')

    return render(request, 'db_product_delete.html')


# Account update :
@login_required
def DashboardOrder(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, "db_orders.html", {'orders': orders})


# Account update :
@login_required
def DashboardOrderDetail(request, oid):
    order = get_object_or_404(Order, oid=oid)

    # Check for BasketLines with the same document number (oid)
    basket_lines = Transaction.objects.filter(oid=oid)
    for basket_line in basket_lines:
        basket_line.total_cost = basket_line.qty * basket_line.price

    return render(request, 'db_order_detail.html', {'order': order, 'basket_lines': basket_lines})
