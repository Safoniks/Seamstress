# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_workertiming'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workertiming',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='workertiming',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
