# Generated by Django 4.0.3 on 2022-03-01 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='logo',
        ),
    ]
