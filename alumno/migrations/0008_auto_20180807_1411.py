# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-07 14:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alumno', '0007_auto_20180807_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procesoalumno',
            name='alumn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumno.Alumno', verbose_name='Alumno'),
        ),
        migrations.AlterField(
            model_name='procesoalumno',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Proceso', verbose_name='Proceso'),
        ),
    ]
