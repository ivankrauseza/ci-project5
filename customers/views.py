from django.shortcuts import render
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
    return render(request, "account_orders.html")


# Account update :
@login_required
def AccountOrderDetail(request):
    return render(request, "account_order_detail.html")
