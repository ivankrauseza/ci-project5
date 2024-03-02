from django.shortcuts import render, get_object_or_404
from shop.models import Order, StripeCustomer, Transaction

from django.contrib.auth.decorators import login_required


# Account index :
@login_required
def AccountIndex(request):
    return render(request, "account_index.html")


# Account update :
@login_required
def AccountUpdate(request):
    return render(request, "account_update.html")


# Account update :
@login_required
def AccountDelete(request):
    return render(request, "account_delete.html")


# Account update :
@login_required
def AccountOrders(request):
    # Get the current user's StripeCustomer
    try:
        stripe_customer = StripeCustomer.objects.get(user=request.user)
    except StripeCustomer.DoesNotExist:
        # Handle the case where the StripeCustomer does not exist for the user
        stripe_customer = None
    
    # If the StripeCustomer exists, retrieve orders associated with the stripe_id
    if stripe_customer:
        orders = Order.objects.filter(sid=stripe_customer.stripe_id).order_by('-created_at')
    else:
        # If no StripeCustomer, you might want to handle this case accordingly
        orders = []

    return render(request, "account_orders.html", {'orders': orders}) 


# Account update :
@login_required
def AccountOrderDetail(request, oid):
    order = get_object_or_404(Order, oid=oid)

    # Check for BasketLines with the same document number (oid)
    basket_lines = Transaction.objects.filter(oid=oid)
    for basket_line in basket_lines:
        basket_line.total_cost = basket_line.qty * basket_line.price

    return render(request, 'account_order_detail.html', {'order': order, 'basket_lines': basket_lines})
