# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-07 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumno', '0003_auto_20180807_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='procesoalumno',
            name='subject',
            field=models.CharField(default='', max_length=128, verbose_name='Materia'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='subjects',
            field=models.ManyToManyField(to='administrador.Materia', verbose_name='Materias'),
        ),
    ]
