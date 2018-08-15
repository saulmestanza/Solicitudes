# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-14 15:49
from __future__ import unicode_literals

import alumno.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumno', '0019_auto_20180814_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historial',
            name='name',
        ),
        migrations.RemoveField(
            model_name='historial',
            name='reviewed_by',
        ),
        migrations.RemoveField(
            model_name='historial',
            name='updated_date',
        ),
        migrations.AddField(
            model_name='historial',
            name='created_by',
            field=models.CharField(default='', max_length=128, verbose_name='Creado Por'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historial',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='documents/%Y/%m/%d', validators=[alumno.validators.validate_file_extension], verbose_name='Documento'),
        ),
        migrations.AddField(
            model_name='historial',
            name='status',
            field=models.CharField(default=' ', max_length=128, verbose_name='Estado'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historial',
            name='description',
            field=models.CharField(max_length=1024, verbose_name='Descripci\xf3n'),
        ),
        migrations.AlterField(
            model_name='procesoalumnoitems',
            name='description',
            field=models.CharField(max_length=1024, verbose_name='Descripci\xf3n'),
        ),
    ]
