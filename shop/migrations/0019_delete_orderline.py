# Generated by Django 4.1.13 on 2024-02-28 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_transaction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderLine',
        ),
    ]
