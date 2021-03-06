# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-10 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0008_auto_20180807_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrera',
            name='cicles',
        ),
        migrations.RemoveField(
            model_name='ciclo',
            name='subjects',
        ),
        migrations.RemoveField(
            model_name='facultad',
            name='carrer',
        ),
        migrations.AddField(
            model_name='carrera',
            name='faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrador.Facultad', verbose_name='Facultad'),
        ),
        migrations.AddField(
            model_name='ciclo',
            name='carrer',
            field=models.ManyToManyField(to='administrador.Carrera', verbose_name='Carreras'),
        ),
        migrations.AddField(
            model_name='materia',
            name='cicles',
            field=models.ManyToManyField(to='administrador.Ciclo', verbose_name='Ciclos'),
        ),
    ]
