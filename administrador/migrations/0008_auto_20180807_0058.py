# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-07 00:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0007_auto_20180803_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historial',
            name='process',
        ),
        migrations.DeleteModel(
            name='Historial',
        ),
    ]
