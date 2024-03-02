from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopIndex, name='shop_index'),
    path('search/', views.ShopSearch, name='shop_search'),
    path('basket/', views.ShopBasket, name='shop_basket'),
    path('basket/delete/<int:basket_item_id>/', views.DeleteBasketItem, name='delete_basket_item'),
    path('basket/update/<int:basket_item_id>/', views.update_basket_item, name='update_basket_item'),
    path('checkout/', views.ShopCheckout, name='shop_checkout'),
    path('orders/', views.ShopOrder, name='shop_order'),
    path('products/<str:sku>/', views.ProductDetail, name='product_detail'),
    path('collection/', views.ShopCollectionList, name='shop_collection_list'),
    path('collection/<slug:collection_slug>/', views.ShopCollection, name='shop_collection'),
    path('newsletter/', views.Newsletter, name='shop_newsletter'),
    # Stripe
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
    path('webhook/', views.stripe_webhook),
    
]
