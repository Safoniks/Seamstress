# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-19 12:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0017_auto_20170819_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='goal',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='worker.Goal'),
        ),
    ]