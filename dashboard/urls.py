from django.urls import path
from . import views
from .views import DashboardProductEdit, FileDeleteView


urlpatterns = [
    path('', views.DashboardIndex, name='db_index'),
    path('products/', views.DashboardProduct, name='db_products'),
    path('products/create/', views.DashboardProductCreate, name='db_product_create'),
    path('products/<str:sku>/', DashboardProductEdit.as_view(), name='db_product_edit'),
    path('products/<int:pk>/delete/', views.DashboardProductDelete, name='db_product_delete'),
    path('products/delete/', views.DashboardProductDelete, name='db_product_delete'),
    path('orders/', views.DashboardOrder, name='db_orders'),
    path('orders/detail/<int:oid>/', views.DashboardOrderDetail, name='db_order_detail'),
    path('product/edit/<sku>/', DashboardProductEdit.as_view(), name='db_product_edit'),
    # path('product/delete_file/<file_id>/', DeleteFileView.as_view(), name='delete_file'),
    path('delete_file/<int:file_id>/', FileDeleteView.as_view(), name='delete_file'),
    
]
