# Generated by Django 4.1.13 on 2024-02-29 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_alter_product_brand_alter_product_desc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='session_id',
            field=models.CharField(max_length=120, null=True),
        ),
    ]