# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-03 20:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0019_auto_20170822_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='end',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='goal',
            name='start',
            field=models.DateTimeField(blank=True),
        ),
    ]
