# Generated by Django 4.1.13 on 2024-02-28 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_rename_product_sku_transaction_sku_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basket',
            old_name='document',
            new_name='oid',
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=10, null=True),
        ),
    ]
