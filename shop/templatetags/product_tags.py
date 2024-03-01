from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django import template
from shop.models import Product, Collection, File


register = template.Library()


@register.inclusion_tag('list/products.html')
def product_items(collection_slug=None, order_by=None):
    collections = None  # Initialize collections to None

    if collection_slug:
        collections = get_object_or_404(Collection, slug=collection_slug)
        filtered_products = Product.objects.filter(blocked='False', category=collections)
    else:
        filtered_products = Product.objects.filter(blocked='False')

    # if order_by:
    if order_by.lower() == 'asc':
        filtered_products = filtered_products.order_by('price')
    elif order_by.lower() == 'desc':
        filtered_products = filtered_products.order_by('-price')

    # Fetch related images for each product
    for product in filtered_products:
        image = File.objects.filter(product=product).first()
        if image and default_storage.exists(image.file.name):
            product.image_url = image.file.url
        else:
            product.image_url = None

    return {
        'product_items': filtered_products,
        'collections': collections,
        'product_count': len(filtered_products)
    }
