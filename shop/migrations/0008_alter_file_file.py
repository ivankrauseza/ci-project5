# Generated by Django 4.1.13 on 2024-02-20 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_orderdeliveryaddress_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(default='', upload_to='uploads/'),
        ),
    ]
