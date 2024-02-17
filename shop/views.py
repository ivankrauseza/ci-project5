from django.shortcuts import render, get_object_or_404
from .models import Product, Collection


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

    # Dictionary of objects :
    context = {
        'product': product,
    }

    return render(request, 'product_detail.html', context)


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
