# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-03 13:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0004_auto_20180803_1309'),
        ('reporteria', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Nombre')),
                ('pdf_file', models.FileField(upload_to='documents/%Y/%m/%d', verbose_name='Reporte')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Descripci\xf3n')),
                ('creation_date', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha Creaci\xf3n')),
                ('updated_date', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha Actualizaci\xf3n')),
                ('created_by', models.CharField(max_length=128, verbose_name='Creador Por')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Proceso',
        ),
        migrations.AddField(
            model_name='reporter',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Proceso', verbose_name='Proceso'),
        ),
    ]
