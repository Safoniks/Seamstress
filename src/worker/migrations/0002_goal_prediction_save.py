# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-15 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='prediction_save',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
