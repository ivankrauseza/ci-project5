from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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
                product=product,
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
@login_required
def ShopBasket(request):
    user_basket_items = Basket.objects.filter(user=request.user)

    # Create a dictionary to store product details
    product_details = {}

    for basket_item in user_basket_items:
        sku = basket_item.product_sku

        # Check if product details for the SKU are already retrieved
        if sku not in product_details:
            product_details[sku] = {
                'name': basket_item.product.name if basket_item.product else 'N/A',
                'price': basket_item.product.price if basket_item.product else 'N/A',
            }

    total_price = 0  # Initialize total price

    # Calculate the price for each line based on quantity * product price
    for basket_item in user_basket_items:
        basket_item.quantity = max(basket_item.quantity, 1)  # Ensure quantity is at least 1
        basket_item.line_price = basket_item.quantity * basket_item.product.price if basket_item.product else 0
        total_price += basket_item.line_price  # Add the line price to the total

    context = {
        'basket_items': user_basket_items,
        'product_details': product_details,
        'total_price': total_price
    }
    return render(request, 'shop_basket.html', context)


# Shop checkout :
@login_required
def ShopCheckout(request):
    return render(request, 'shop_checkout.html')


# Shop checkout :
@login_required
def ShopOrder(request):
    return render(request, 'shop_order.html')


# Shop customer :
def ShopAccount(request):
    return render(request, 'shop_account.html')
