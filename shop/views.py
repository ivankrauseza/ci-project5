from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Collection, Basket, OrderDeliveryAddress
from .forms import AddToBasketForm, OrderDeliveryAddressForm


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
    
    image = product.files.first()

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
        'product_in_basket': product_in_basket,
        'product_image_url': image.file.url if image and default_storage.exists(image.file.name) else None
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

    try:
        user_delivery_address = OrderDeliveryAddress.objects.get(customer=request.user)
    except OrderDeliveryAddress.DoesNotExist:
        user_delivery_address = None

    if user_delivery_address:
        order_address_form = OrderDeliveryAddressForm(instance=user_delivery_address)
    else:
        order_address_form = OrderDeliveryAddressForm(request.POST or None)
        
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

    if request.method == 'POST' and 'delete_address' in request.POST:
        user_delivery_address.delete()
        return redirect('shop_basket')

    if request.method == 'POST' and 'street_address' in request.POST:
        order_address_form = OrderDeliveryAddressForm(request.POST)

        if order_address_form.is_valid():
            address_queryset = OrderDeliveryAddress.objects.filter(customer=request.user)

            if address_queryset.exists():
                order_address_instance = address_queryset.first()
            else:
                order_address_instance = OrderDeliveryAddress(customer=request.user)

            order_address_instance.name = order_address_form.cleaned_data['name']
            order_address_instance.phone = order_address_form.cleaned_data['phone']
            order_address_instance.street_address = order_address_form.cleaned_data['street_address']
            order_address_instance.city = order_address_form.cleaned_data['city']
            order_address_instance.state = order_address_form.cleaned_data['state']
            order_address_instance.postal_code = order_address_form.cleaned_data['postal_code']
            order_address_instance.save()

            return redirect('shop_basket')

    context = {
        'basket_items': user_basket_items,
        'product_details': product_details,
        'total_price': total_price,
        'order_address_form': order_address_form,
        'user_delivery_address': user_delivery_address,
    }
    return render(request, 'shop_basket.html', context)


@login_required
def DeleteBasketItem(request, basket_item_id):
    basket_item = get_object_or_404(Basket, id=basket_item_id, user=request.user)

    # Perform the deletion
    basket_item.delete()

    return redirect('shop_basket')

@login_required
def update_basket_item(request, basket_item_id):
    basket_item = get_object_or_404(Basket, id=basket_item_id, user=request.user)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))

        # Update the quantity
        basket_item.quantity = max(new_quantity, 1)
        basket_item.save()

    return redirect('shop_basket')


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
