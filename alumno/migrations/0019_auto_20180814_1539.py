# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-14 15:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumno', '0018_auto_20180814_0414'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historial',
            old_name='process',
            new_name='process_alumno',
        ),
        migrations.RenameField(
            model_name='procesoalumnoitems',
            old_name='process',
            new_name='process_alumno',
        ),
    ]