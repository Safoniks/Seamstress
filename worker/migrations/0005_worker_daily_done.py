# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0004_worker_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='last_reset_done',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
