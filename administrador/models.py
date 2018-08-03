# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import formats, timezone
from django.utils.translation import ugettext as _

class UserProfile(models.Model):
    user = models.OneToOneField(User)

class Facultad(models.Model):
    name = models.CharField(max_length=128, verbose_name=_(u'Nombre'))
    carrer = models.ManyToManyField('Carrera', verbose_name=_(u'Carreras'))
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Carrera(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'Nombre'))
    cicles = models.ManyToManyField('Ciclo', verbose_name=_(u'Ciclos'))
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s"%(self.name)

class Ciclo(models.Model):
    name = models.CharField(max_length=128, verbose_name=_(u'Nombre'))
    subjects = models.ManyToManyField('Materia', verbose_name=_(u'Materias'))
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Materia(models.Model):
    name = models.CharField(max_length=128, verbose_name=_(u'Nombre'))
    description = models.CharField(max_length=128, verbose_name=_(u'Descripción'), blank=True, null=True)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Proceso(models.Model):
    name = models.CharField(max_length=128, verbose_name=_(u'Nombre'))
    proceso_items = models.ManyToManyField('ProcesoItems', verbose_name=_(u'Descripción'))
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s"%(self.name)

class ProcesoItems(models.Model):
    name = models.CharField(max_length=128, verbose_name=_(u'Nombre'))
    description = models.CharField(max_length=256, verbose_name=_(u'Descripción'))
    image = models.ImageField(verbose_name=u'Imágen', upload_to='documents/%Y/%m/%d', blank=True, null=True)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s"%(self.name)


class Historial(models.Model):
    STATUS_CHOICE=[
    ('IN' , u'Ingresado'),
    ('ET' , u'En tránsito'),
    ('CN' , u'Cancelado'),
    ('AC' , u'Acceptado'),
    ]
    process = models.ForeignKey(Proceso, on_delete=models.CASCADE, verbose_name=_('Proceso'))
    name = models.CharField(max_length=128, verbose_name=_(u'Nombre'))
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICE,
        default='IN',
        verbose_name=_('Estado'),
        )
    description = models.CharField(max_length=256, verbose_name=_(u'Descripción'))
    creation_date = models.DateField(default=timezone.now, verbose_name=_('Fecha Creación'))
    updated_date = models.DateField(default=timezone.now, verbose_name=_('Fecha Actualización'))
    reviewed_by = models.CharField(max_length=128, verbose_name=_(u'Revisado Por'))
    approved_by = models.CharField(max_length=128, verbose_name=_(u'Aprobado Por'))
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s"%(self.name)


class Periodo(models.Model):
    name = models.CharField(max_length=128, verbose_name=_(u'Periodo'))
    carrer = models.ManyToManyField('Carrera', verbose_name=_(u'Carrera'))
    deleted = models.BooleanField(default=False, verbose_name=_('Activo'))
    
    def __unicode__(self):
        return "%s"%(self.name)

