# Generated by Django 4.1.13 on 2024-02-18 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_order_alter_basket_options_orderline'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='product',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
        ),
    ]