# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OperationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('duration', models.PositiveIntegerField()),
                ('cost_per_second', models.FloatField()),
                ('full_cost', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
