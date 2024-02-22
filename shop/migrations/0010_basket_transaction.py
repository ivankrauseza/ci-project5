# Generated by Django 4.1.13 on 2024-02-22 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_stripecustomer'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='transaction',
            field=models.CharField(choices=[('D', 'Default'), ('E', 'Error'), ('S', 'Sales Order'), ('B', 'Basket Item'), ('P', 'Stock Purchase')], default='D', max_length=1),
        ),
    ]
