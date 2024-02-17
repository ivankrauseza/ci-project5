from django.shortcuts import get_object_or_404
from django import template
from shop.models import Product, Collection


register = template.Library()


@register.inclusion_tag('list/products.html')
def product_items(collection_slug=None, order_by=None):

    print(collection_slug)

    if collection_slug:
        collections = get_object_or_404(Collection, slug=collection_slug)
        products = Product.objects.filter(category=collections)
    else:
        collections = None
        products = Product.objects.all()

    if order_by == 'asc':
        products = products.order_by('price')
    elif order_by == 'desc':
        products = products.order_by('-price')

    return {
        'product_items': products,
        'collections': collections,
        'product_count': len(products)
    }
