from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Collections Model :
class Collection(models.Model):

    class Meta:
        verbose_name_plural = "Collections"

    catname = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.catname


# Products Model :
class Product(models.Model):

    class Meta:
        verbose_name_plural = "Products"

    sku = models.CharField(max_length=255, default='', unique=True)
    name = models.CharField(max_length=255, default='')
    blurb = models.TextField(default='')
    desc = models.TextField(default='')
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    category = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.CharField(max_length=255, default='')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    blocked = models.BooleanField(default=False)
    type_choices = [
        ('PHYSICAL', 'Physical'),
        ('DIGITAL', 'Digital'),
        ('SUBSCRIPTION', 'Subscription'),
        ('LABOUR', 'Labour'),
    ]
    type = models.CharField(
        max_length=20,
        choices=type_choices,
        default='PHYSICAL',
        )

    def __str__(self):
        return self.name


# Files Model
class File(models.Model):

    class Meta:
        verbose_name_plural = "Files"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='files'
        )
    file = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product.sku}"


# Basket :
class Basket(models.Model):

    class Meta:
        verbose_name_plural = "Basket Lines"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, default=None)
    product_sku = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Basket Item {self.id}"


# Orders :
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255, unique=True)
    delivery_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.username}"
    

# Order lines :
class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_lines')
    product_sku = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.order.order_number}, Product SKU: {self.product_sku}"


class OrderDeliveryAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Ireland")
    phone = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"{self.customer}'s Address"
