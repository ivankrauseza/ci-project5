from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Collection, Basket
from .forms import AddToBasketForm


# Shop index :
def ShopIndex(request):
    products = Product.objects.all()

    # Dictionary of objects :
    context = {
        'products': products,
    }

    return render(request, 'shop_index.html', context)


# Shop detail :
def ProductDetail(request, sku):
    product = get_object_or_404(Product, sku=sku)
    max_quantity = int(Product.objects.get(sku=sku).stock)
    form = AddToBasketForm(max_quantity, request.POST)

    if request.user.is_authenticated:
        product_in_basket = Basket.objects.filter(user=request.user, product_sku=product.sku).exists()
    else:
        product_in_basket = False

    if request.method == 'POST':
        form = AddToBasketForm(max_quantity, request.POST)
        if form.is_valid():
            # Add the product to the basket with the specified quantity
            quantity = form.cleaned_data['quantity']
            Basket.objects.create(
                user=request.user,
                product_sku=product.sku,
                quantity=quantity,
                price=product.price
            )
            return redirect('product_detail', sku=sku)
    else:
        form = AddToBasketForm(max_quantity)

    return render(request, 'product_detail.html', {
        'form': form,
        'product': product,
        'product_in_basket': product_in_basket
    })


# Shop collection :
def ShopCollection(request, collection_slug=None):
    collection = get_object_or_404(Collection, slug=collection_slug)
    return render(request, 'shop_collection.html', {'collection': collection})


# Shop search :
def ShopSearch(request):
    return render(request, 'shop_search.html')


# Shop basket :
def ShopBasket(request):
    return render(request, 'shop_basket.html')


# Shop checkout :
def ShopCheckout(request):
    return render(request, 'shop_checkout.html')


# Shop checkout :
def ShopOrder(request):
    return render(request, 'shop_order.html')


# Shop customer :
def ShopAccount(request):
    return render(request, 'shop_account.html')
