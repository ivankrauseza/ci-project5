# Generated by Django 4.1.13 on 2024-02-28 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_rename_delivery_address_order_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='oda',
        ),
    ]