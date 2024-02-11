from django.shortcuts import render


# Shop index :
def ShopIndex(request):
    return render(request, 'shop_index.html')


# Shop collection :
def ShopCollection(request):
    return render(request, 'shop_collection.html')


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
