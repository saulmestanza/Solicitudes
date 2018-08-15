# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from functools import partial
from models import *
from administrador.forms import CarreraForm

class ReporterForm(forms.ModelForm):

    class Meta:
        model = Reporter
        fields = (
            'process',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(ReporterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, *args, **kw):
        super(ReporterForm, self).save(*args, **kw)
        return ReporterForm


