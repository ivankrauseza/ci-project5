from django import template
from shop.models import Collection


register = template.Library()


@register.inclusion_tag('menu/menu_collection.html')
def menu_items():
    items = Collection.objects.all()
    return {'menu_items': items}
