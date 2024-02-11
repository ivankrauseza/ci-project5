from django.shortcuts import render


# Account index :
def AccountIndex(request):
    return render(request, "account_index.html")


# Account update :
def AccountUpdate(request):
    return render(request, "account_update.html")


# Account update :
def AccountDelete(request):
    return render(request, "account_delete.html")


# Account update :
def AccountOrders(request):
    return render(request, "account_orders.html")


# Account update :
def AccountOrderDetail(request):
    return render(request, "account_order_detail.html")
