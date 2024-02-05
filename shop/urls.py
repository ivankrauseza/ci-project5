from django.urls import path
from . import views


urlpatterns = [
    path('', views.ShopIndex, name='shop_index'),
]
