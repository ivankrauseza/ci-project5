from django.core.files.storage import default_storage

import stripe #stripe
from django.conf import settings # stripe
from django.http.response import JsonResponse, HttpResponse # stripe
from django.views.decorators.csrf import csrf_exempt # stripe

from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Collection, Transaction, OrderDeliveryAddress, StripeCustomer, Order
from .forms import AddToBasketForm, OrderDeliveryAddressForm
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal, ROUND_HALF_UP
import time


# Email
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
        product_in_basket = Transaction.objects.filter(
            user=request.user,
            type="B",
            sku=product.sku
        ).exists()
    else:
        product_in_basket = False
    
    image = product.files.first()

    if request.method == 'POST':
        form = AddToBasketForm(max_quantity, request.POST)
        if form.is_valid():
            # Add the product to the basket with the specified quantity
            qty = form.cleaned_data['qty']
            Transaction.objects.create(
                user=request.user,
                product=product,
                sku=product.sku,
                sid=scid,
                qty=qty,
                price=product.price,
                type="B"
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
    user_basket_items = Transaction.objects.filter(
        user=request.user,
        type="B"
    )

    try:
        user_delivery_address = OrderDeliveryAddress.objects.get(user=request.user)
    except OrderDeliveryAddress.DoesNotExist:
        user_delivery_address = None

    if user_delivery_address:
        order_address_form = OrderDeliveryAddressForm(instance=user_delivery_address)
    else:
        order_address_form = OrderDeliveryAddressForm(request.POST or None)
        
    # Create a dictionary to store product details
    product_details = {}

    for basket_item in user_basket_items:
        sku = basket_item.sku

        # Check if product details for the SKU are already retrieved
        if sku not in product_details:
            product_details[sku] = {
                'name': basket_item.product.name if basket_item.product else 'N/A',
                'price': basket_item.product.price if basket_item.product else 'N/A',
            }

    total_price = 0  # Initialize total price

    # Calculate the price for each line based on quantity * product price
    for basket_item in user_basket_items:
        basket_item.qty = max(basket_item.qty, 1)  # Ensure quantity is at least 1
        basket_item.line_price = basket_item.qty * basket_item.product.price if basket_item.product else 0
        total_price += basket_item.line_price  # Add the line price to the total

    if request.method == 'POST' and 'delete_address' in request.POST:
        user_delivery_address.delete()
        return redirect('shop_basket')

    if request.method == 'POST' and 'street' in request.POST:
        order_address_form = OrderDeliveryAddressForm(request.POST)

        if order_address_form.is_valid():
            address_queryset = OrderDeliveryAddress.objects.filter(user=request.user)

            if address_queryset.exists():
                order_address_instance = address_queryset.first()
            else:
                order_address_instance = OrderDeliveryAddress(user=request.user)

            order_address_instance.name = order_address_form.cleaned_data['name']
            order_address_instance.phone = order_address_form.cleaned_data['phone']
            order_address_instance.street = order_address_form.cleaned_data['street']
            order_address_instance.city = order_address_form.cleaned_data['city']
            order_address_instance.state = order_address_form.cleaned_data['state']
            order_address_instance.postal_code = order_address_form.cleaned_data['postal_code']
            order_address_instance.save()
            # Update sid using the save_stripe_id method
            order_address_instance.save_stripe_id()

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
    basket_item = get_object_or_404(Transaction, id=basket_item_id, user=request.user)

    # Perform the deletion
    basket_item.delete()

    return redirect('shop_basket')

@login_required
def update_basket_item(request, basket_item_id):
    basket_item = get_object_or_404(Transaction, id=basket_item_id, user=request.user)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('qty', 1))

        # Update the quantity
        basket_item.qty = max(new_quantity, 1)
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


# STRIPE CHECKOUT
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


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

        try:
            basket_items = Transaction.objects.filter(
                user=request.user,
                type="B"
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
                        'quantity': basket_item.qty,
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
        print(e)
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(e)
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        
        # Get session objects :
        session = event['data']['object']
        session_id = session.get('id')
        sid = session.get('customer')
        customer_email = session.customer_details.get('email')
        total_amount = session.get('amount_total') / 100
        total_amount_decimal = Decimal(str(total_amount))
        currency = session.get('currency')

        last_order = Order.objects.order_by('-oid').first()

        if last_order and last_order.oid.isdigit():
            sequence = str(int(last_order.oid) + 1)
        else:
            # Use a more dynamic or configurable fallback value
            sequence = '1000000000'

        order_address_queryset = OrderDeliveryAddress.objects.filter(sid=sid)
        if order_address_queryset.exists():
            order_address = order_address_queryset.first()
            combined_text = order_address.get_combined_address_text()
        else:
            # Handle the case when no matching object is found.
            combined_text = "No matching order address found."

        # Create a new Order in Django:
        order = Order(
            oid=sequence,  # Order ID
            oda=combined_text,  # Address Snapshot
            sid=sid,
            session_id=session_id,
            customer_email=customer_email,
            total_amount=total_amount_decimal,
            currency=currency,
            status='Order Received',
            paid='PAID'
        )
        order.save()

        basket_items = Transaction.objects.filter(
            sid=sid,
            type="B"
        )
        for basket_item in basket_items:
            basket_item.oid = sequence
            basket_item.type = "S"
            basket_item.save()

    return HttpResponse(status=200)
