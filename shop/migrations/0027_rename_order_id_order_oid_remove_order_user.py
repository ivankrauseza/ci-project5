# Generated by Django 4.1.13 on 2024-02-28 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_rename_street_address_orderdeliveryaddress_street'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_id',
            new_name='oid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]