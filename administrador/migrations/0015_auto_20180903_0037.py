# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-03 00:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0014_proceso_requirements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Nombre'),
        ),
    ]