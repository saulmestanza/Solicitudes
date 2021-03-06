# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-03 13:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0003_auto_20180803_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Nombre')),
                ('description', models.CharField(max_length=256, verbose_name='Descripci\xf3n')),
                ('creation_date', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha Creaci\xf3n')),
                ('updated_date', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha Actualizaci\xf3n')),
                ('reviewed_by', models.CharField(max_length=128, verbose_name='Revisado Por')),
                ('approved_by', models.CharField(max_length=128, verbose_name='Aprobado Por')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Proceso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Nombre')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProcesoItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Nombre')),
                ('description', models.CharField(max_length=256, verbose_name='Descripci\xf3n')),
                ('image', models.ImageField(blank=True, null=True, upload_to='documents/%Y/%m/%d', verbose_name='Im\xe1gen')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='proceso',
            name='proceso_items',
            field=models.ManyToManyField(to='administrador.ProcesoItems', verbose_name='Descripci\xf3n'),
        ),
        migrations.AddField(
            model_name='historial',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Proceso', verbose_name='Proceso'),
        ),
    ]
