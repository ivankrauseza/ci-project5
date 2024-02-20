from django.urls import path
from . import views


urlpatterns = [
    path('', views.ShopIndex, name='shop_index'),
    path('collection/', views.ShopCollection, name='shop_collection'),
    path('search/', views.ShopSearch, name='shop_search'),
    path('basket/', views.ShopBasket, name='shop_basket'),
    path('basket/delete/<int:basket_item_id>/', views.DeleteBasketItem, name='delete_basket_item'),
    path('basket/update/<int:basket_item_id>/', views.update_basket_item, name='update_basket_item'),
    
    path('checkout/', views.ShopCheckout, name='shop_checkout'),
    path('orders/', views.ShopOrder, name='shop_order'),
    path('products/<str:sku>/', views.ProductDetail, name='product_detail'),
    path('collection/', views.ShopCollection, name='shop_collection'),
    path('collection/<slug:collection_slug>/', views.ShopCollection, name='shop_collection'),
]
