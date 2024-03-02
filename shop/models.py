from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from django.dispatch import receiver
from allauth.account.signals import user_signed_up

from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# START 1. When a user signs up, they need to be assigned a stripe account :
class StripeCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s StripeCustomer"


@receiver(user_signed_up)
def create_or_update_user_profile(sender, user, **kwargs):
    customer = stripe.Customer.create(email=user.email)
    StripeCustomer.objects.get_or_create(
        user=user,
        defaults={'stripe_id': customer.id}
    )
# END 1.


# START 2. Collections/Categories
class Collection(models.Model):

    class Meta:
        verbose_name_plural = "Collections"

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.name
# END 2.


# START 3. Products
class Product(models.Model):

    class Meta:
        verbose_name_plural = "Products"

    sku = models.CharField(max_length=255, default='', unique=True)
    name = models.CharField(max_length=255, default='')
    blurb = models.TextField(default='')
    desc = models.TextField(default='', null=True)
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    category = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.CharField(max_length=255, default='cadence')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
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
# END 3.


# START 4. Files for Products
class File(models.Model):

    class Meta:
        verbose_name_plural = "Files"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='files'
        )
    file = models.FileField(upload_to='cadence/', default="")
    type = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product.sku}"
# end 4.


# Basket :
class Basket(models.Model):

    class Meta:
        verbose_name_plural = "Basket Lines"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, default=None)
    product_sku = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    customer_id = models.CharField(max_length=120, null=True)
    oid = models.CharField(max_length=20, default="0000000000")
    price = models.DecimalField(max_digits=10, decimal_places=2)
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


# Transaction :
class Transaction(models.Model):

    class Meta:
        verbose_name_plural = "Transaction Lines"

    TYPE_CHOICES = [
        ('D', 'Default'),
        ('E', 'Error'),
        ('S', 'Sales Order'),
        ('B', 'Basket Item'),
        ('P', 'Stock Purchase'),
    ]
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default="D")
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None)
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default=None)
    sku = models.CharField(max_length=255)
    sid = models.CharField(max_length=120, null=True)
    oid = models.CharField(max_length=20, default="0000000000")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Basket Item {self.id}"


# START 11.
class OrderDeliveryAddress(models.Model): 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sid = models.CharField(max_length=255, default="")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Ireland")
    phone = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"{self.user}'s Address"
    
    def get_combined_address_text(self):
        fields = [
            f"Contact Person: {self.name}",
            f"Phone: {self.phone}",
            f"Address: {self.street}, {self.city}, {self.state}",
            f"Postal Code: {self.postal_code}",
            f"Country: {self.country}"
            ]
        combined_text = "\n".join(filter(None, fields))
        return combined_text
    
    def save_stripe_id(self):
        # Assuming user can have only one StripeCustomer
        stripe_customer = StripeCustomer.objects.filter(user=self.user).first()
        if stripe_customer:
            self.sid = stripe_customer.stripe_id
            self.save()
# END 11.


# START 12.
class Order(models.Model):
    oid = models.CharField(max_length=120, unique=True, null=True)  # Unique identifier for the order
    sid = models.CharField(max_length=120, null=True)  # Stripe Session ID for the payment
    session_id = models.CharField(max_length=120, null=True)  # Stripe Session ID for the payment
    customer_email = models.EmailField(default="")  # Email address of the customer
    oda = models.TextField() # Lock the address
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Timestamp when the order was created
    updated_at = models.DateTimeField(auto_now=True, null=True)  # Timestamp for the last update
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Total amount charged
    currency = models.CharField(max_length=3, null=True)  # Currency code, e.g., 'USD'
    status = models.CharField(max_length=30, default='pending', null=True)  # Order status (e.g., pending, paid, fulfilled, canceled)
    paid = models.CharField(max_length=30, default='False')

    def __str__(self):
        return f"Order {self.oid}"
# END 12.
