# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0006_auto_20170814_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workertiming',
            name='delta',
        ),
        migrations.AlterField(
            model_name='workertiming',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
