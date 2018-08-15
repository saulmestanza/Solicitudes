# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import formats, timezone
from django.utils.translation import ugettext as _
from administrador.models import Proceso

class Reporter(models.Model):
    process = models.ForeignKey(Proceso, on_delete=models.CASCADE, verbose_name=_('Proceso'))
    pdf_file = models.FileField(
		verbose_name=u'Reporte',
		upload_to='documents/%Y/%m/%d'
	)
    creation_date = models.DateField(default=timezone.now, verbose_name=_('Fecha Creación'))
    created_by = models.CharField(max_length=128, verbose_name=_(u'Creador Por'))
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s"%(self.name)