# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-22 05:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumno', '0022_auto_20180815_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nota',
            name='description',
        ),
        migrations.AlterField(
            model_name='nota',
            name='nota',
            field=models.CharField(max_length=5, verbose_name='Nota'),
        ),
    ]
