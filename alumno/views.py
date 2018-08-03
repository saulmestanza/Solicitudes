# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.http import Http404
from django.db.models import Q
from django.conf import settings
from django.forms.utils import ErrorList
from forms import *
from models import *
from administrador.models import *

# Create your views here.
class AlumnoCreate(CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumno/alumno_create.html'
    success_url = '/'

    def form_invalid(self, form):
        return super(AlumnoCreate, self).form_invalid(form)

    def get(self, request, next=None):
        return super(AlumnoCreate, self).get(request)

    def form_valid(self, form):
        try:
            if User.objects.filter(username=form.instance.user.username).exists():
                errors = form._errors.setdefault("email", ErrorList())
                errors.append(u"Ya existe un usuario registrado con este email")
                response = super(AlumnoCreate, self).form_invalid(form)
                # print(User.objects.filter(username=form.instance.user.username))
            else:
                response = super(AlumnoCreate, self).form_valid(form)
        except Exception, e:
            print 'Error', e
            errors = form._errors.setdefault("email", ErrorList())
            errors.append(u"Ya existe un usuario registrado con este email")
            if form.instance.user.id:
                form.instance.user.delete()
            response = super(AlumnoCreate, self).form_invalid(form)
        return response
    
    def get_context_data(self, **kwargs):
        context = super(AlumnoCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Crear Usuario"
        return context


class AlumnoHistorialListView(UserPassesTestMixin, ListView):
    model = Alumno
    template_name = 'alumno/alumno_historial.html'

    
    def test_func(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super(AlumnoHistorialListView, self).get_context_data(**kwargs)
        context['tittle'] = "Seguimiento de Trámites"
        context['motto'] = "Bandeja de seguimiento"
        context['procesos'] = Proceso.objects.filter(deleted=False)
        context['table_id'] = "alumno"
        return context


class AlumnoTramiteCreate(UserPassesTestMixin, CreateView):
    model = Historial
    fields = '__all__'
    template_name = 'alumno/alumno_tramite_create.html'
    success_url = '/alumno/alumno-seguimiento/'

    
    def test_func(self):
        return self.request.user.is_staff

    
    def get_context_data(self, **kwargs):
        context = super(AlumnoTramiteCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Crear Solicitud"
        context['motto'] = "Llene todos los datos"

        context['periodos'] = Periodo.objects.all()
        context['procesos'] = Proceso.objects.all()
        context['ciclos'] = Ciclo.objects.all()
        context['carreras'] = Carrera.objects.all()
        context['materias'] = Materia.objects.all()

        form = context['form']
        for field in form.fields:
            form.fields[field].widget.attrs['class'] = 'form-control'
            if form.fields[field].help_text:
                form.fields[field].widget.attrs['data-toggle'] = 'tooltip'
                form.fields[field].widget.attrs['data-placement'] = 'top'
                form.fields[field].widget.attrs['title'] = form.fields[field].help_text
        return context
    
