# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import formats, timezone
from administrador.models import *
from .validators import validate_file_extension

class Alumno(models.Model):
    user = models.OneToOneField(User)
    carrer = models.ForeignKey(Carrera, on_delete=models.CASCADE, verbose_name=_('Carrera'), null=True)
    token = models.CharField(max_length=256, blank=True, default='')
    deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False, verbose_name=_('Activo'))
    
    def __unicode__(self):
        return "%s %s"%(self.user.first_name, self.user.last_name)

class Nota(models.Model):
    profesor = models.CharField(max_length=256, verbose_name=_(u'Profesor'))
    nota = models.CharField(max_length=256, verbose_name=_(u'Nota'))
    description = models.CharField(max_length=1024, verbose_name=_(u'Descripción'), blank=True, null=True)
    creation_date = models.DateField(default=timezone.now, verbose_name=_('Fecha Creación'))

class ProcesoAlumno(models.Model):
    STATUS_CHOICE=[
    ('IN' , u'Ingresado'),
    ('ET' , u'En tránsito'),
    ('CN' , u'Cancelado'),
    ('RC' , u'Rechazado'),
    ('ER' , u'En Revisión'),
    ('FN' , u'Finalizado'),
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
    subject = models.ForeignKey(Materia, on_delete=models.CASCADE, verbose_name=_('Materia'))
    parcial = models.CharField(max_length=256, verbose_name=_(u'Parcial'), blank=True, null=True)
    periodo = models.CharField(max_length=256, verbose_name=_(u'Periodo'), blank=True, null=True)
    notes = models.ManyToManyField(Nota)
    document = models.FileField(verbose_name=u'Documento', upload_to='documents/%Y/%m/%d', blank=True, null=True, validators=[validate_file_extension])
    deleted = models.BooleanField(default=False)
    
    def status_verbose(self):
        return dict(ProcesoAlumno.STATUS_CHOICE)[self.status]

    def __unicode__(self):
        return "%s - %s"%(self.process.name, self.subject.name)


class ProcesoAlumnoItems(models.Model):
    process_alumno = models.ForeignKey(ProcesoAlumno, on_delete=models.CASCADE, verbose_name=_('Proceso'))
    name = models.CharField(max_length=128, verbose_name=_(u'Tema'))
    description = models.CharField(max_length=1024, verbose_name=_(u'Descripción'))
    creation_date = models.DateField(default=timezone.now, verbose_name=_('Fecha Creación'))
    document = models.FileField(verbose_name=u'Documento', upload_to='documents/%Y/%m/%d', blank=True, null=True, validators=[validate_file_extension])
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s"%(self.name)


class Historial(models.Model):
    process_alumno = models.ForeignKey(ProcesoAlumno, on_delete=models.CASCADE, verbose_name=_('Proceso Alumno'))
    status = models.CharField(max_length=128, verbose_name=_(u'Estado'))
    description = models.CharField(max_length=1024, verbose_name=_(u'Descripción'))
    creation_date = models.DateField(default=timezone.now, verbose_name=_('Fecha Creación'))
    document = models.FileField(verbose_name=u'Documento', upload_to='documents/%Y/%m/%d', blank=True, null=True, validators=[validate_file_extension])
    created_by = models.CharField(max_length=128, verbose_name=_(u'Creado Por'))
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s - %s"%(self.process_alumno, self.status)


