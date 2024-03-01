from django.urls import path
from . import views


urlpatterns = [
    path('', views.AccountIndex, name='account_index'),
    path('update/', views.AccountUpdate, name='account_update'),
    path('delete/', views.AccountDelete, name='account_delete'),
    path('orders/', views.AccountOrders, name='account_orders'),
    path('orders/detail/<int:oid>/', views.AccountOrderDetail, name='account_order_detail'),

]
