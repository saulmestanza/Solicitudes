# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import formats, timezone
from administrador.models import *

class Alumno(models.Model):
    user = models.OneToOneField(User)
    carrer = models.ForeignKey(Carrera, on_delete=models.CASCADE, verbose_name=_('Carrera'), null=True)
    token = models.CharField(max_length=256, blank=True, default='')
    deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False, verbose_name=_('Activo'))
    
    def __unicode__(self):
        return "%s %s"%(self.user.first_name, self.user.last_name)

class ProcesoAlumno(models.Model):
    STATUS_CHOICE=[
    ('IN' , u'Ingresado'),
    ('ET' , u'En tránsito'),
    ('CN' , u'Cancelado'),
    ('AC' , u'Aceptado'),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICE,
        default='IN',
        verbose_name=_('Estado'),
        )
    process = models.ForeignKey(Proceso, on_delete=models.CASCADE, verbose_name=_('Proceso'))
    alumn = models.ForeignKey(Alumno, on_delete=models.CASCADE, verbose_name=_('Alumno'))
    creation_date = models.DateField(default=timezone.now, verbose_name=_('Fecha Creación'))
    subject = models.CharField(max_length=128, verbose_name=_(u'Materia'), default='', null=True, blank=True)
    deleted = models.BooleanField(default=False)
    
    def status_verbose(self):
        return dict(ProcesoAlumno.STATUS_CHOICE)[self.status]

    def __unicode__(self):
        return "%s - %s %s - %s"%(self.process.name, self.alumn.user.first_name, self.alumn.user.last_name, self.subject)


class ProcesoAlumnoItems(models.Model):
    process = models.ForeignKey(ProcesoAlumno, on_delete=models.CASCADE, verbose_name=_('Proceso'))
    name = models.CharField(max_length=128, verbose_name=_(u'Tema'))
    description = models.CharField(max_length=256, verbose_name=_(u'Descripción'))
    creation_date = models.DateField(default=timezone.now, verbose_name=_('Fecha Creación'))
    image = models.ImageField(verbose_name=u'Imágen', upload_to='documents/%Y/%m/%d', blank=True, null=True)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s"%(self.name)


class Historial(models.Model):
    process = models.ForeignKey(ProcesoAlumno, on_delete=models.CASCADE, verbose_name=_('Proceso Alumno'))
    name = models.CharField(max_length=128, verbose_name=_(u'Nombre'))
    description = models.CharField(max_length=256, verbose_name=_(u'Descripción'))
    creation_date = models.DateField(default=timezone.now, verbose_name=_('Fecha Creación'))
    updated_date = models.DateField(default=timezone.now, verbose_name=_('Fecha Actualización'))
    reviewed_by = models.CharField(max_length=128, verbose_name=_(u'Revisado Por'))
    approved_by = models.CharField(max_length=128, verbose_name=_(u'Aprobado Por'))
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s"%(self.name)
