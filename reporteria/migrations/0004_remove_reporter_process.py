# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-30 09:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporteria', '0003_auto_20180815_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporter',
            name='process',
        ),
    ]
