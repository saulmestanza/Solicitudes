# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-15 13:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporteria', '0002_auto_20180803_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporter',
            name='description',
        ),
        migrations.RemoveField(
            model_name='reporter',
            name='name',
        ),
        migrations.RemoveField(
            model_name='reporter',
            name='updated_date',
        ),
    ]