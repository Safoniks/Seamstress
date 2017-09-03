# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0005_worker_daily_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='last_reset_salary',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='worker',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
