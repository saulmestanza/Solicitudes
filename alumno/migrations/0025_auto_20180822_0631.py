# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-22 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumno', '0024_procesoalumno_extras'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procesoalumno',
            name='status',
            field=models.CharField(choices=[(b'IN', 'Ingresado'), (b'ER', 'En Revisi\xf3n'), (b'ET', 'En Tr\xe1nsito'), (b'CN', 'Cancelado'), (b'RL', 'Rechazado por Alumno'), (b'AL', 'Aceptado por Alumno'), (b'FN', 'Finalizado')], default='IN', max_length=2, verbose_name='Estado'),
        ),
    ]
