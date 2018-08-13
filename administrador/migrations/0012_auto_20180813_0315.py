# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-13 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0011_auto_20180810_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='No Activo'),
        ),
        migrations.AlterField(
            model_name='ciclo',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='No Activo'),
        ),
        migrations.AlterField(
            model_name='facultad',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='No Activo'),
        ),
        migrations.AlterField(
            model_name='materia',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='No Activo'),
        ),
        migrations.AlterField(
            model_name='periodo',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='No Activo'),
        ),
        migrations.AlterField(
            model_name='proceso',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='No Activo'),
        ),
    ]