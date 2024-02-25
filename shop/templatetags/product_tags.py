from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django import template
from shop.models import Product, Collection, File


register = template.Library()


@register.inclusion_tag('list/products.html')
def product_items(collection_slug=None, order_by=None):

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
    else:
        # Handle the case where order_by is not provided
        # Default to no specific ordering
        products = products.all()

    # Fetch related images for each product
    for product in products:
        image = File.objects.filter(product=product).first()
        product.image_url = image.file.url if image and default_storage.exists(image.file.name) else None

    return {
        'product_items': products,
        'collections': collections,
        'product_count': len(products)
    }
