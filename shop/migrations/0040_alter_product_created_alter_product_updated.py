# Generated by Django 4.1.13 on 2024-03-02 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0039_alter_orderdeliveryaddress_sid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
