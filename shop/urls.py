from django.urls import path
from . import views


urlpatterns = [
    path('', views.ShopIndex, name='shop_index'),
    path('collection/', views.ShopCollection, name='shop_collection'),
    path('search/', views.ShopSearch, name='shop_search'),
    path('basket/', views.ShopBasket, name='shop_basket'),
    path('checkout/', views.ShopCheckout, name='shop_checkout'),
    path('orders/', views.ShopOrder, name='shop_order'),
]
