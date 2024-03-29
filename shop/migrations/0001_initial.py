# Generated by Django 4.1.13 on 2024-02-06 22:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catname', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Collections',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(default='', max_length=255, unique=True)),
                ('name', models.CharField(default='', max_length=255)),
                ('blurb', models.TextField(default='')),
                ('desc', models.TextField(default='')),
                ('stock', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default='0.00', max_digits=10)),
                ('brand', models.CharField(default='', max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('blocked', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('PHYSICAL', 'Physical'), ('DIGITAL', 'Digital'), ('SUBSCRIPTION', 'Subscription'), ('LABOUR', 'Labour')], default='PHYSICAL', max_length=20)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.collection')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='shop.product')),
            ],
            options={
                'verbose_name_plural': 'ProductFiles',
            },
        ),
    ]
