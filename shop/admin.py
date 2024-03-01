from django.contrib import admin
from .models import Collection, Product, File, Basket, Transaction, Order, StripeCustomer, OrderDeliveryAddress


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_id')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'price', 'stock', 'blocked')
    list_filter = ('category', 'blocked')
    search_fields = ('sku', 'name')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('product', 'file', 'type', 'description')
    search_fields = ('product__sku', 'file', 'type', 'description')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'sku', 'qty', 'price', 'created_at')
    search_fields = ('user__username', 'sku')
    list_filter = ('created_at', 'user')

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('oid',)


@admin.register(OrderDeliveryAddress)
class OrderDeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('user',)
