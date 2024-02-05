from django.shortcuts import render


# Create your views here.
def ShopIndex(request):
    return render(request, 'shop_index.html')
