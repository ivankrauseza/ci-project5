# Generated by Django 4.1.13 on 2024-02-22 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_basket_customer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_number',
        ),
    ]