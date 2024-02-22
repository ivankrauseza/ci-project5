from django.contrib import admin
from .models import Collection, Product, File, Basket, Order, OrderLine, StripeCustomer


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('catname', 'slug')
    prepopulated_fields = {'slug': ('catname',)}
    search_fields = ('catname',)


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


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'product_sku', 'quantity', 'price', 'created_at')
    search_fields = ('user__username', 'product_sku')
    list_filter = ('created_at', 'user')

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User'


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'delivery_address', 'order_date')
    search_fields = ('order_number', 'user__username')
    inlines = [OrderLineInline]

@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_sku', 'quantity', 'price')
    search_fields = ('order__order_number', 'product_sku')
