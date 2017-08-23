# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-22 14:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operationtype', '0003_auto_20170822_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationtype',
            name='cost_per_second',
        ),
        migrations.AlterField(
            model_name='operationtype',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='operationtypecategory.OperationTypeCategory'),
            preserve_default=False,
        ),
    ]