from django.core.files.storage import default_storage
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Collection, Basket, OrderDeliveryAddress, StripeCustomer, Order
from .forms import AddToBasketForm, OrderDeliveryAddressForm
import time

# Email
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


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

    # Logged In - Get Stripe ID :
    try:
        if request.user.is_authenticated:
            customer = StripeCustomer.objects.get(user=request.user)
            scid = customer.stripe_id
        else:
            customer = None
            scid = None
    except StripeCustomer.DoesNotExist:
        customer = None
        scid = None

    if request.user.is_authenticated:
        product_in_basket = Basket.objects.filter(
            user=request.user,
            transaction="B",
            product_sku=product.sku
        ).exists()
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
                customer_id=scid,
                product=product,
                product_sku=product.sku,
                quantity=quantity,
                price=product.price,
                transaction="B"
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
    user_basket_items = Basket.objects.filter(
        user=request.user,
        transaction="B"
    )

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


class SuccessView(TemplateView):
    template_name = 'checkout_success.html'


class CancelledView(TemplateView):
    template_name = 'checkout_cancelled.html'


# Stripe Config :
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


# CHECKOUT SESSION :
@csrf_exempt
def create_checkout_session(request):

    # Logged In - Get Stripe ID :
    try:
        customer = StripeCustomer.objects.get(user=request.user)
        scid = customer.stripe_id

    # Logged Out :
    except StripeCustomer.DoesNotExist:
        scid = None
        # Guest checkout...

    scheme = request.scheme
    domain = request.get_host()
    
    if request.method == 'GET':
        domain_url = f'{scheme}://{domain}/'
        # domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            basket_items = Basket.objects.filter(
                user=request.user,
                transaction="B"
            )
            if basket_items.exists():
                stripe_line_items = []
                for basket_item in basket_items:
                    stripe_line_items.append({
                        'price_data': {
                            'currency': 'eur',
                            'unit_amount': int(basket_item.price * 100),
                            'product_data': {
                                'name': basket_item.product.name,
                            },
                        },
                        'quantity': basket_item.quantity,
                    })

            # Create new Checkout Session for the order
            checkout_session = stripe.checkout.Session.create(
                customer=scid,
                success_url=domain_url + 'success/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=stripe_line_items,
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


# STRIPE WEBHOOKS :
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        
        # Get session objects :
        session = event['data']['object']
        session_id = session.get('id')
        customer_id = session.get('customer')
        customer_email = session.customer_details.get('email')
        total_amount = session.get('amount_total') / 100
        total_amount_decimal = Decimal(str(total_amount))
        currency = session.get('currency')

        # Generate order number :
        timestamp = int(time.time())
        sequence = str(timestamp)

        # Create a new Order in Django:
        order = Order(
            order_id=sequence,
            stripe_session_id=str(session_id),
            customer_id=str(customer_id),
            customer_email=str(customer_email),
            total_amount=total_amount_decimal,
            currency=str(currency),
            status='paid'
        )
        order.save()

        basket_items = Basket.objects.filter(
            customer_id=customer_id,
            transaction="B"
        )
        for basket_item in basket_items:
            basket_item.document = sequence
            basket_item.transaction = "S"
            basket_item.save()

    return HttpResponse(status=200)