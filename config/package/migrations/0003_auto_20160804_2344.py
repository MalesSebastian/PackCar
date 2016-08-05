# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-04 23:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0002_auto_20160804_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='drivers.Driver'),
        ),
    ]
