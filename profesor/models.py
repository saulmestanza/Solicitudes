# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from administrador.models import Materia

class Profesor(models.Model):
    user = models.OneToOneField(User)
    subjects = models.ManyToManyField(Materia)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s %s"%(self.user.first_name, self.user.last_name)