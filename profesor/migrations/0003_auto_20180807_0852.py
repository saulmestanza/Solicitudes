# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-07 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesor', '0002_remove_profesor_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesor',
            name='subjects',
            field=models.ManyToManyField(to='administrador.Materia', verbose_name='Materias'),
        ),
    ]
