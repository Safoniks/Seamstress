# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0003_auto_20170804_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='goal',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
