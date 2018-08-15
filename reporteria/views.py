# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import DeleteView, TemplateView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import update_session_auth_hash
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.db.models import Q
from django.template import loader
from django.conf import settings
from django.forms.utils import ErrorList
from django.utils.timezone import datetime #important if using timezones
from models import *
from forms import *
from profesor.models import *
from administrador.models import *
from alumno.models import *
import json
import random
import string
import os

class ReporteriaNotasCreateView(PermissionRequiredMixin, CreateView):
    model = Reporter
    form_class = ReporterForm

    template_name = 'reporteria/reporter_notas.html'
    success_url = '/reporteria/reporteria-notas/'
    permission_required = (
        'reporteria.add_reporter',
    )

    def test_func(self):
        return self.request.user

    def form_valid(self, form):
        clean = form.cleaned_data
        description =  clean['description']
        document = clean['documento']
        try:
            context = self.get_context_data()
            self.object = form.save()
            response = super(ReporteriaNotasCreateView, self).form_valid(form)
        except Exception as e:
            print e
            response = super(ReporteriaNotasCreateView, self).form_invalid(form)
        return response

    def form_invalid(self, form):
        return super(ReporteriaNotasCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ReporteriaNotasCreateView, self).get_context_data(**kwargs)
        context['tittle'] = "Repoteria"
        context['carrers'] = Carrera.objects.filter(deleted=False)
        context['periodos'] = Periodo.objects.filter(deleted=False)
        context['proceso_alumno'] = ProcesoAlumno.objects.filter(status='FN')
        context['motto'] = "Reporteria Notas"
        return context



class ReporteriaEstadisticasCreateView(PermissionRequiredMixin, CreateView):
    model = Reporter
    form_class = ReporterForm

    template_name = 'reporteria/reporter_estadisticas.html'
    success_url = '/reporteria/reporteria-estadisticas/'
    permission_required = (
        'reporteria.add_reporter',
    )

    def test_func(self):
        return self.request.user

    def form_valid(self, form):
        clean = form.cleaned_data
        description =  clean['description']
        document = clean['documento']
        try:
            context = self.get_context_data()
            self.object = form.save()
            response = super(ReporteriaEstadisticasCreateView, self).form_valid(form)
        except Exception as e:
            print e
            response = super(ReporteriaEstadisticasCreateView, self).form_invalid(form)
        return response

    def form_invalid(self, form):
        return super(ReporteriaEstadisticasCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ReporteriaEstadisticasCreateView, self).get_context_data(**kwargs)
        context['tittle'] = "Repoteria"
        context['carrers'] = Carrera.objects.filter(deleted=False)
        context['periodos'] = Periodo.objects.filter(deleted=False)
        context['proceso_alumno'] = ProcesoAlumno.objects.filter(status='FN')
        context['motto'] = "Reporteria Estadísticas"
        return context

