# Generated by Django 4.1.13 on 2024-02-26 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_order_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.CharField(default='False', max_length=30),
        ),
    ]
