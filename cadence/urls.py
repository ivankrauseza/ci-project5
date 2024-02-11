from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('', include('pages.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('account/', include('customers.urls')),
]
