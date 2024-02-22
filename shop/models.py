from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.dispatch import receiver
from allauth.account.signals import user_signed_up

from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@receiver(user_signed_up)
def create_or_update_user_profile(sender, user, **kwargs):
    customer = stripe.Customer.create(email=user.email)
    StripeCustomer.objects.get_or_create(
        user=user,
        defaults={'stripe_id': customer.id}
    )


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
    file = models.FileField(upload_to='uploads/', default="")
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
    customer_id = models.CharField(max_length=120, null=True)
    document = models.CharField(max_length=20, default="0000000000")
    TRANSACTION_CHOICES = [
        ('D', 'Default'),
        ('E', 'Error'),
        ('S', 'Sales Order'),
        ('B', 'Basket Item'),
        ('P', 'Stock Purchase'),
    ]
    transaction = models.CharField(max_length=1, choices=TRANSACTION_CHOICES, default="D")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Basket Item {self.id}"


# Orders :
class Order(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # order_number = models.CharField(max_length=255, unique=True)
    delivery_address = models.TextField()
    # order_date = models.DateTimeField(auto_now_add=True)
    # Stripe Webhook
    order_id = models.CharField(max_length=120, unique=True, null=True)  # Unique identifier for the order
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Timestamp when the order was created
    updated_at = models.DateTimeField(auto_now=True, null=True)  # Timestamp for the last update
    stripe_session_id = models.CharField(max_length=120, null=True)  # Stripe Session ID for the payment
    customer_id = models.CharField(max_length=120, null=True)  # Stripe Customer ID
    customer_email = models.EmailField(default="")  # Email address of the customer
    stripe_session_id = models.CharField(max_length=120, null=True)  # Stripe Session ID for the payment
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Total amount charged
    currency = models.CharField(max_length=3, null=True)  # Currency code, e.g., 'USD'
    status = models.CharField(max_length=30, default='pending', null=True)  # Order status (e.g., pending, paid, fulfilled, canceled)

    def __str__(self):
        return f"Order {self.order_id}"
    

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
    

class StripeCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s StripeCustomer"
