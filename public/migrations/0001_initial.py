# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('operationtype', '0001_initial'),
        ('product', '0004_product_operations'),
        ('worker', '0007_auto_20170809_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerOperationLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.PositiveIntegerField(default=0)),
                ('cost', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('operation_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='operationtype.OperationType')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Product')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worker.Worker')),
            ],
        ),
    ]
