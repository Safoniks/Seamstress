# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-15 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.FloatField()),
                ('salary', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'payroll',
                'db_table': 'payroll',
                'verbose_name_plural': 'payrolls',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='WorkerOperationLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.PositiveIntegerField(default=0)),
                ('cost', models.FloatField(blank=True)),
                ('duration', models.PositiveIntegerField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'worker operation log',
                'db_table': 'worker_operation_logs',
                'verbose_name_plural': 'worker operation logs',
            },
        ),
        migrations.CreateModel(
            name='WorkerTiming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('start', 'start'), ('stop', 'stop'), ('reset', 'reset')], max_length=5)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'worker timing',
                'db_table': 'worker_timing',
                'verbose_name_plural': 'worker timings',
                'ordering': ['date'],
            },
        ),
    ]
