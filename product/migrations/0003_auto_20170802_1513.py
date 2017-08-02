# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20170731_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productphoto',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_photos', to='product.Product'),
        ),
    ]
