# Generated by Django 4.1.13 on 2024-02-28 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_rename_quantity_transaction_qty'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='transaction',
            new_name='type',
        ),
    ]
